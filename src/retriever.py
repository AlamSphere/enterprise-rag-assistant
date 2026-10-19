import re
from src.access_control import filter_documents_by_role

# Expanded Enterprise Knowledge Base Documents
DOCUMENTS = [
    {
        "doc_id": "it_support_guide",
        "title": "IT Support & Ticketing Guide",
        "department": "it",
        "allowed_roles": ["employee", "hr", "finance", "admin"],
        "text": "Employees can submit an IT support ticket by visiting portal.company.local/it or emailing support@company.com with urgent issue details."
    },
    {
        "doc_id": "public_employee_handbook",
        "title": "Public Employee Handbook",
        "department": "hr",
        "allowed_roles": ["employee", "hr", "finance", "admin"],
        "text": "Standard working hours are 9:00 AM to 5:00 PM Monday through Friday. Lunch breaks are 1 hour long."
    },
    {
        "doc_id": "employee_leave_guide",
        "title": "Employee Leave & Holidays Standard",
        "department": "hr",
        "allowed_roles": ["employee", "hr", "finance", "admin"],
        "text": "All full-time employees receive 20 annual paid leave days along with 10 paid public holidays per calendar year."
    },
    {
        "doc_id": "remote_work_policy",
        "title": "Remote Work & Hybrid Guidelines",
        "department": "operations",
        "allowed_roles": ["employee", "hr", "finance", "admin"],
        "text": "Employees are permitted to work remotely up to 2 days per week with team manager approval and an active VPN connection."
    },
    {
        "doc_id": "office_dress_code",
        "title": "Office Dress Code Standard",
        "department": "hr",
        "allowed_roles": ["employee", "hr", "finance", "admin"],
        "text": "The company observes a business casual dress code from Monday through Thursday, and casual attire on Fridays."
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

# Stopwords to ignore common structural English words
STOPWORDS = {"what", "is", "the", "are", "our", "do", "i", "how", "to", "a", "an", "of", "for", "in", "on", "can", "where", "does", "time"}

def tokenize(text: str):
    """Tokenizes text into lowercase words while stripping common stopwords."""
    words = re.findall(r'\w+', text.lower())
    return set(w for w in words if w not in STOPWORDS)

def search_documents(query: str, user_role: str = "employee", top_k: int = 1):
    """
    1. Filters documents using server-side RBAC rules.
    2. Scores documents based on meaningful keyword overlap.
    """
    authorized_docs = filter_documents_by_role(DOCUMENTS, user_role)

    if not authorized_docs:
        return []

    query_tokens = tokenize(query)
    if not query_tokens:
        return []

    scored_docs = []

    for doc in authorized_docs:
        doc_tokens = tokenize(doc["text"] + " " + doc["title"])
        overlap = len(query_tokens.intersection(doc_tokens))
        
        # Only accept documents that match meaningful query keywords
        if overlap > 0:
            scored_docs.append((overlap, doc))

    # Sort documents by highest keyword match score
    scored_docs.sort(key=lambda x: x[0], reverse=True)

    if scored_docs:
        return [doc for _, doc in scored_docs[:top_k]]

    # If no relevant document matches, return empty list (prevents repeated loop/fallback)
    return []
