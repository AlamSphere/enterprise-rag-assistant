import math
from collections import Counter
import re
from src.access_control import filter_documents_by_role

# Enterprise Knowledge Base Documents
DOCUMENTS = [
    {
        "doc_id": "it_support_guide",
        "title": "IT Support & Ticketing Guide",
        "department": "it",
        "allowed_roles": ["employee", "hr", "finance", "admin"],
        "text": "Employees can submit an IT support ticket by visiting the internal portal at portal.company.local/it or emailing support@company.com with urgent issue details."
    },
    {
        "doc_id": "public_employee_handbook",
        "title": "Public Employee Handbook",
        "department": "hr",
        "allowed_roles": ["employee", "hr", "finance", "admin"],
        "text": "Standard working hours are 9:00 AM to 5:00 PM. All employees receive 20 days of paid annual leave per year along with national holidays."
    },
    {
        "doc_id": "hr_leave_policy",
        "title": "HR Confidential Leave & Payroll Policy",
        "department": "hr",
        "allowed_roles": ["hr", "admin"],
        "text": "HR Specialists manage paid leave approvals. Annual leave consists of 20 statutory days plus 5 discretionary days approved by department managers."
    },
    {
        "doc_id": "hr_compensation_policy",
        "title": "Salary Review & Compensation Standard",
        "department": "hr",
        "allowed_roles": ["hr", "admin"],
        "text": "Salary reviews take place annually in Q4. Compensation increases depend on performance band ratings and executive budget sign-off."
    },
    {
        "doc_id": "finance_expense_policy",
        "title": "Expense Reimbursement Protocol",
        "department": "finance",
        "allowed_roles": ["finance", "admin"],
        "text": "Expense reports must be submitted within 30 days of purchase using receipts. Travel allowances are capped at $150/day for lodging."
    }
]

def tokenize(text: str):
    """Simple regex tokenization for TF-IDF matching."""
    return re.findall(r'\w+', text.lower())

def compute_tfidf_similarity(query: str, documents: list):
    """Computes basic TF-IDF similarity between query and candidate documents."""
    query_tokens = tokenize(query)
    if not query_tokens:
        return []

    results = []
    for doc in documents:
        doc_tokens = tokenize(doc["text"])
        doc_counts = Counter(doc_tokens)
        
        # Calculate term overlap score
        score = sum(doc_counts[token] for token in query_tokens if token in doc_counts)
        if score > 0:
            results.append((score, doc))

    # Sort documents by relevance score descending
    results.sort(key=lambda x: x[0], reverse=True)
    return [doc for _, doc in results]

def search_documents(query: str, user_role: str = "employee", top_k: int = 3):
    """
    1. Filters documents using server-side RBAC rules.
    2. Runs TF-IDF similarity search over authorized documents.
    """
    # Filter documents based on active user role
    authorized_docs = filter_documents_by_role(DOCUMENTS, user_role)

    if not authorized_docs:
        return []

    # Retrieve relevant matching documents
    matched_docs = compute_tfidf_similarity(query, authorized_docs)
    
    # If query terms don't match specific keywords, return top authorized documents as context
    if not matched_docs:
        return authorized_docs[:top_k]

    return matched_docs[:top_k]
