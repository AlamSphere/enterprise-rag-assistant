
# Roles recognized by our application.
VALID_ROLES = {"employee", "hr", "finance", "admin"}


def filter_documents(documents, user_role):
    """
    Return only documents the user's role is allowed to access.
    """

    # Reject unknown roles instead of granting access by default.
    if not isinstance(user_role, str) or user_role not in VALID_ROLES:
        raise ValueError("Invalid or unauthorized user role")

    authorized_documents = []

    for document in documents:
        allowed_roles = document.get("allowed_roles", [])

        # Fail closed if the permission metadata is malformed.
        if not isinstance(allowed_roles, list):
            continue

        if user_role in allowed_roles:
            authorized_documents.append(document)

    return authorized_documents
s