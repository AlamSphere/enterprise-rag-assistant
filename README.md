# Enterprise RAG Assistant&#x20;

**An AI-powered enterprise knowledge assistant that retrieves relevant company documents, generates grounded answers, and demonstrates role-based document access control.**

## 📌 Overview

Enterprise RAG Assistant is a Retrieval-Augmented Generation (RAG) application designed to answer questions using enterprise knowledge sources rather than relying exclusively on a language model's pretrained knowledge.

The application combines a Python backend, a document retrieval pipeline, a Hugging Face language model integration, and a React chat interface.

The project explores how enterprise AI assistants can provide useful answers while restricting document retrieval according to user roles.

### Why build this project?

General-purpose language models can generate convincing answers even when they lack access to a company's actual policies. Enterprise applications need a way to retrieve relevant evidence, control access to confidential information, and identify the sources behind an answer.

This project serves as a practical foundation for exploring those challenges.

## ✨ Features

- **Retrieval-Augmented Generation:** Retrieves relevant company documents to provide context for answers.
- **Role-Based Access Control (RBAC) demonstration:** Filters documents according to the selected user role.
- **LLM integration:** Uses Hugging Face inference for natural-language answer generation when correctly configured.
- **Source references:** Returns document titles, identifiers, and department metadata alongside answers.
- **REST API:** Uses FastAPI to expose the question-answering endpoint.
- **Interactive chat UI:** Built with React and Vite.
- **Configurable inference:** Keeps the Hugging Face token on the backend.
- **Modular Python code:** Separates retrieval, access control, document handling, and API functionality.

> **Security note:** The current role selector is intended for demonstration. A role supplied by a client is not proof of identity. Production deployments require verified authentication and server-enforced permissions.

## 🏗️ Architecture

```text
                  User
                   |
                   v
          React + Vite Frontend
                   |
                   | POST /api/query
                   v
             FastAPI Backend
                   |
                   v
        Role-Based Document Filtering
                   |
                   v
          Document Retrieval
          (TF-IDF / lexical search)
                   |
                   v
         Relevant Document Context
                   |
                   v
         Hugging Face Inference
                   |
                   v
       Answer + Retrieved Sources
                   |
                   v
            React Chat UI
```

### Technology stack

| Component       | Technology                 | Purpose                             |
| --------------- | -------------------------- | ----------------------------------- |
| Frontend        | React, Vite                | Chat interface and user interaction |
| Styling         | CSS / utility classes      | User interface presentation         |
| Backend         | Python, FastAPI            | API and request handling            |
| Validation      | Pydantic                   | Request schema validation           |
| Retrieval       | TF-IDF / lexical matching  | Finding relevant documents          |
| Language model  | Hugging Face Hub inference | Generating natural-language answers |
| Access control  | Python role filtering      | Restricting document retrieval      |
| Version control | Git and GitHub             | Source management and collaboration |

## 📂 Project structure

The following is the intended high-level structure. File names may vary slightly in your current checkout.

```text
enterprise-rag-assistant/
├── src/
│   ├── app.py
│   ├── retriever.py
│   ├── access_control.py
│   ├── document_loader.py
│   ├── chunking.py
│   └── demo_access.py
├── data/
│   └── sample_documents/
├── tests/
│   ├── test_access_control.py
│   ├── test_document_loader.py
│   └── test_retriever.py
├── frontend/
│   ├── src/
│   │   ├── App.jsx
│   │   ├── main.jsx
│   │   ├── App.css
│   │   └── index.css
│   ├── package.json
│   └── index.html
├── .env.example
├── .gitignore
├── requirements.txt
└── README.md
```

## ⚙️ Prerequisites

Install the following before running the project:

- Python 3.10 or newer
- Node.js and npm
- Git
- A Hugging Face account and access to a compatible inference model, if using live LLM generation
- A code editor such as Visual Studio Code

Check your installations:

```bash
python --version
node --version
npm --version
git --version
```

## 🚀 Getting started

### 1. Clone the repository

```bash
git clone https://github.com/AlamSphere/enterprise-rag-assistant.git
cd enterprise-rag-assistant
```

### 2. Create a Python virtual environment

**Windows PowerShell:**

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
```

If PowerShell blocks activation, you can invoke the environment's Python executable directly instead.

### 3. Install Python dependencies

```powershell
python -m pip install --upgrade pip
pip install -r requirements.txt
```

Ensure `requirements.txt` includes the dependencies actually used by your current backend, including FastAPI, Uvicorn, Pydantic, `huggingface_hub`, and any retrieval libraries.

### 4. Configure Hugging Face

Create a `.env` file in the repository root:

```dotenv
HF_TOKEN=your_hugging_face_token
HF_MODEL_ID=your_supported_model_id
```

Use a model identifier that is available through your Hugging Face inference provider. Update the backend to read `HF_MODEL_ID` if the current code still hard-codes the model name.

**Never commit `.env` or publish your access token.** Create a `.env.example` file containing placeholders instead:

```dotenv
HF_TOKEN=your_token_here
HF_MODEL_ID=your_model_id_here
```

If the model provider is unavailable or the token lacks permission, generation may fail until the configuration is corrected.

### 5. Start the backend

Run this command from the repository root:

```powershell
python -m uvicorn src.app:app --reload
```

The API should be available at:

- API root: [http://127.0.0.1:8000/](http://127.0.0.1:8000/)
- Interactive API documentation: [http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs)

Open the documentation page to inspect and test the API endpoints.

### 6. Start the frontend

Open a second terminal:

```powershell
cd frontend
npm install
npm run dev
```

Open the local URL printed by Vite, commonly:

[http://localhost:5173/](http://localhost:5173/)

Keep both the backend and frontend terminals running while using the application.

## 💬 How to use the application

1. Open the frontend in your browser.
2. Select a demo role from the sidebar.
3. Ask a question about one of the available enterprise documents.
4. Wait for the backend to retrieve authorized documents and generate a response.
5. Review the displayed answer and source references.
6. Change the role and repeat the query to observe how accessible documents differ.

### Example questions

| Question                                         | Expected source or behavior                                      |
| ------------------------------------------------ | ---------------------------------------------------------------- |
| Where can I submit an IT support ticket?         | IT Support & Ticketing Guide                                     |
| What are the standard working hours?             | Public Employee Handbook                                         |
| How many discretionary leave days are available? | HR Leave Policy, for authorized roles                            |
| When do salary reviews take place?               | Salary Review & Compensation Standard, for authorized roles      |
| What is the lodging allowance limit?             | Expense Reimbursement Protocol, for authorized roles             |
| What is the company cafeteria menu?              | Should not invent an answer if no relevant document is available |

These are expected test scenarios, not a claim that every query has already been verified. Actual results depend on the current retrieval implementation, role configuration, and model availability.

## 🔌 API reference

### `GET /`

Checks whether the API service is responding.

Example:

```bash
curl http://127.0.0.1:8000/
```

### `POST /api/query`

Submits a question to the retrieval and generation pipeline.

Example request:

```json
{
  "query": "Where do I submit an IT ticket?",
  "user_role": "employee"
}
```

Example response shape:

```json
{
  "answer": "Example answer grounded in the retrieved company document.",
  "sources": [
    {
      "id": "it_support_guide",
      "title": "IT Support & Ticketing Guide",
      "department": "it"
    }
  ]
}
```

The response above illustrates the API contract. Exact fields depend on the current backend implementation.

## 🔐 Role-based access control

The sample knowledge base demonstrates four roles:

| Role     | Intended access                                    |
| -------- | -------------------------------------------------- |
| Employee | General employee handbook and IT support guide     |
| HR       | Public documents and HR policies                   |
| Finance  | Public documents, IT support, and finance policies |
| Admin    | All sample documents                               |

The backend should filter documents **before** passing any content to the language model.

This reduces the risk of unauthorized content being exposed through model-generated responses.

However, the demo role selector is not a production identity system. In a real deployment, permissions must be derived from an authenticated identity and enforced server-side. Additional controls are needed for document ingestion, logging, caching, and stored conversation history.

## 🧠 How RAG works in this project

Retrieval-Augmented Generation combines information retrieval with language-model generation.

1. **Question:** The user submits a natural-language query.
2. **Authorization:** The backend determines which documents are accessible under the active role.
3. **Retrieval:** The search module ranks accessible documents for relevance.
4. **Context construction:** Relevant document text is assembled into the prompt.
5. **Generation:** The language model receives the question and retrieved context.
6. **Response:** The backend returns the answer and source metadata to the frontend.

### Current retrieval approach

The initial prototype uses lexical retrieval. TF-IDF and cosine similarity can provide a useful baseline for a small document collection.

Lexical search has limitations: it may fail to recognize semantically similar phrases when they use different words. A future version can evaluate embedding-based retrieval and compare its performance against the baseline.

## 🛠️ Challenges encountered and lessons learned

### 1. Python imports and application entry points

**Challenge:** Running the application from different directories can cause Python package imports to fail or load the wrong application module.

**Lesson:** Use a consistent repository root and a single documented FastAPI entry point. Running `python -m uvicorn src.app:app --reload` from the root makes the intended module explicit.

### 2. React bootstrap and JSX configuration

**Challenge:** JSX syntax requires the appropriate build configuration and file handling. A mismatched entry-point filename or import can prevent Vite from starting.

**Lesson:** Keep the React bootstrap consistent with the actual file names, use `.jsx` for JSX-containing files, and verify imports before debugging the API.

### 3. Local model setup and inference availability

**Challenge:** The initial local-model approach using Ollama did not work in the development environment.

**Approach:** The project moved to Hugging Face inference to explore hosted language-model generation instead.

**Lesson:** Model availability, authentication, provider support, and API errors are separate concerns. A working Python application does not guarantee that a remote model endpoint is available.

### 4. Repetitive or irrelevant responses

**Challenge:** Different questions could produce similar responses.

**Root causes identified in the earlier implementation:**

- Retrieval based on word overlap could rank irrelevant documents.
- The retriever could return arbitrary authorized documents when no matches were found.
- The prompt used only the first retrieved document even when multiple documents were returned.
- Model failures could silently trigger a fallback response, making it unclear whether an LLM had generated the answer.

**Improvements:** Use explicit relevance scoring, return no matches when appropriate, include the relevant retrieved context, log inference failures, and test retrieval independently of generation.

### 5. Keeping answers grounded in evidence

**Challenge:** A language model may produce plausible information not supported by company documents.

**Lesson:** Prompt instructions alone are not a guarantee of factual correctness. The application should test answer grounding, provide source references, handle missing evidence, and avoid generating unsupported policy details.

### 6. Protecting confidential documents

**Challenge:** A frontend-selected role is easy for a user to change.

**Lesson:** A role selector is useful for demonstrating RBAC, but production access control requires authentication and server-side authorization before retrieval.

## 🧪 Testing

Run the existing automated tests from the repository root:

```powershell
python -m pytest -v
```

If `pytest` is not installed:

```powershell
pip install pytest
```

Recommended tests include:

- Valid and invalid user roles.
- Authorized versus unauthorized document retrieval.
- Relevant queries and queries with no matching documents.
- Correct source metadata in API responses.
- Empty or excessively long requests.
- Hugging Face timeout, authentication, and provider failures.
- Frontend handling of successful and failed API requests.
- Verification that unauthorized document text never reaches the LLM prompt.

The number of passing tests should be reported only after running them against the current code.

## 🐛 Troubleshooting

| Problem                               | What to check                                                                                      |
| ------------------------------------- | -------------------------------------------------------------------------------------------------- |
| `ModuleNotFoundError`                 | Activate the virtual environment, install dependencies, and run Uvicorn from the repository root.  |
| API connection error in React         | Confirm that FastAPI is running and that the frontend calls the correct backend URL.               |
| CORS error                            | Check the allowed frontend origin in the FastAPI CORS configuration.                               |
| Hugging Face authentication error     | Verify `HF_TOKEN`, token permissions, and that the token is loaded from the repository root.       |
| Model unavailable                     | Check the configured model ID and whether the inference provider supports it.                      |
| Repeated or irrelevant answers        | Inspect retrieved documents and relevance scores before changing the prompt.                       |
| Empty source list                     | Check document loading, access filtering, and retrieval results.                                   |
| Vite compilation error                | Check JSX syntax, entry-point filenames, dependencies, and imports.                                |
| Sensitive documents appear in answers | Stop testing with confidential data and inspect server-side authorization and prompt construction. |

## ⚠️ Current limitations

This project is a learning and prototyping implementation, not a production-certified enterprise system.

- The sample knowledge base is small and may be hard-coded.
- Lexical retrieval does not provide full semantic understanding.
- Model output can still be inaccurate or unsupported.
- Inference depends on external provider availability and credentials.
- The demo role selector does not establish a verified user identity.
- Production authentication, authorization, monitoring, and deployment hardening require additional work.
- Conversation persistence, large-scale ingestion, and scalable vector search should be considered future improvements unless implemented and tested separately.

## 🗺️ Roadmap

- [ ] Validate the complete React-to-FastAPI-to-LLM workflow.
- [ ] Improve retrieval evaluation and no-match behavior.
- [ ] Add embedding-based semantic search.
- [ ] Implement document ingestion and configurable chunking.
- [ ] Add verified authentication and production-grade RBAC.
- [ ] Improve source citations and answer-grounding tests.
- [ ] Add conversation history and follow-up question support.
- [ ] Add structured logging, request limits, and monitoring.
- [ ] Create deployment instructions and automated CI tests.

## 🤝 Contributing

Contributions and suggestions are welcome.

1. Fork the repository.
2. Create a feature branch.
3. Make a focused change.
4. Add or update tests.
5. Open a pull request describing the change and its validation.

## 🔒 Security

Do not commit API tokens, passwords, private documents, or production credentials.

Before using this project with real enterprise information, implement and test authentication, server-side authorization, appropriate data handling, and safe logging practices.

Please report security vulnerabilities privately to the repository maintainer rather than publishing sensitive exploit details.

## 👨‍💻 Author

**Md Abu Sufiyan Alam**

Artificial Intelligence & Machine Learning Engineering Graduate

- GitHub: [@AlamSphere](https://github.com/AlamSphere)
- Project: [Enterprise RAG Assistan](https://github.com/AlamSphere/enterprise-rag-assistant)t

---

\<p align="center">   Built to explore secure, evidence-grounded AI assistants for enterprise knowledge retrieval. \</p>
