
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

from src.access_control import filter_documents
from src.document_loader import load_documents
from src.chunking import chunk_text


def search_documents(query, user_role, top_k=3):
    """Search authorized document chunks using TF-IDF similarity."""

    if not isinstance(query, str) or not query.strip():
        raise ValueError("query must be a non-empty string")

    if not isinstance(top_k, int) or isinstance(top_k, bool) or top_k < 1:
        raise ValueError("top_k must be a positive integer")

    # Enforce role-based filtering before building the search corpus.
    documents = filter_documents(load_documents(), user_role)

    chunks = []
    for document in documents:
        for chunk in chunk_text(
            document["content"],
            chunk_size=500,
            overlap=100,
        ):
            chunks.append({
                "document_id": document["id"],
                "title": document["title"],
                "department": document["department"],
                "text": chunk,
            })

    if not chunks:
        return []

    # Fit only on content the current role is authorized to access.
    texts = [chunk["text"] for chunk in chunks]
    vectorizer = TfidfVectorizer(
        lowercase=True,
        stop_words="english",
    )

    try:
        document_vectors = vectorizer.fit_transform(texts)
        query_vector = vectorizer.transform([query])
    except ValueError:
        # For example, every chunk might contain only stop words.
        return []

    scores = cosine_similarity(query_vector, document_vectors).flatten()
    ranked_indices = scores.argsort()[::-1]

    results = []

    for index in ranked_indices:
        score = float(scores[index])

        # Avoid presenting irrelevant matches as useful evidence.
        if score <= 0:
            continue

        result = chunks[index].copy()
        result["score"] = score
        results.append(result)

        if len(results) >= top_k:
            break

    return results
