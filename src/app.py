import os
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

try:
    from dotenv import load_dotenv
    load_dotenv()
except ImportError:
    pass

try:
    from huggingface_hub import InferenceClient
except ImportError:
    InferenceClient = None

from src.retriever import search_documents

app = FastAPI(title="Enterprise RAG Assistant API")

# Enable CORS for React frontend (running on http://localhost:5173)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

HF_TOKEN = os.getenv("HF_TOKEN")
hf_client = InferenceClient(token=HF_TOKEN) if (HF_TOKEN and InferenceClient) else None

class QueryRequest(BaseModel):
    query: str
    user_role: str = "employee"

@app.get("/")
def read_root():
    return {"status": "ok", "message": "Enterprise RAG Assistant API is running!"}

@app.post("/api/query")
def handle_query(request: QueryRequest):
    if not request.query.strip():
        raise HTTPException(status_code=400, detail="Query cannot be empty.")

    # 1. Retrieve authorized document chunks based on user role
    retrieved_chunks = search_documents(request.query, request.user_role, top_k=3)

    if not retrieved_chunks:
        return {
            "answer": f"No documents found matching '{request.query}' accessible under the '{request.user_role}' role.",
            "sources": []
        }

    # 2. Extract top retrieved text content
    top_text = retrieved_chunks[0].get("text", "")
    
    # 3. Generate response using Hugging Face or fallback summary
    answer = ""
    if hf_client:
        try:
            prompt = f"Based on the following enterprise document, answer the question accurately.\n\nDocument: {top_text}\n\nQuestion: {request.query}\nAnswer:"
            response = hf_client.text_generation(prompt, model="HuggingFaceH4/zephyr-7b-beta", max_new_tokens=150)
            answer = response.strip()
        except Exception:
            answer = f"According to enterprise records: {top_text}"
    else:
        answer = f"According to enterprise records: {top_text}"

    # 4. Prepare structured source citations for frontend
    sources = [
        {
            "id": chunk.get("doc_id", "unknown"),
            "title": chunk.get("title", chunk.get("doc_id")),
            "department": chunk.get("department", "general")
        }
        for chunk in retrieved_chunks
    ]

    return {
        "answer": answer,
        "sources": sources
    }
