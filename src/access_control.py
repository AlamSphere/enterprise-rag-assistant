# Access Control Rules and RBAC Security Logic

ROLE_HIERARCHY = {
    "admin": ["admin", "finance", "hr", "employee"],
    "finance": ["finance", "employee"],
    "hr": ["hr", "employee"],
    "employee": ["employee"]
}

def filter_documents_by_role(documents: list, user_role: str = "employee") -> list:
    """
    Filters a list of document dicts based on the user's role.
    
    Each document should have an 'allowed_roles' list (e.g. ['employee', 'hr']).
    If 'allowed_roles' is missing, it defaults to public ('employee').
    """
    user_role = user_role.lower().strip()
    accessible_roles = ROLE_HIERARCHY.get(user_role, ["employee"])

    filtered_docs = []
    for doc in documents:
        allowed = doc.get("allowed_roles", ["employee"])
        # Check if any role accessible by user overlaps with document allowed roles
        if any(role in accessible_roles for role in allowed):
            filtered_docs.append(doc)

    return filtered_docs
