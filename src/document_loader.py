
import json
from pathlib import Path


# Find the project root, regardless of the terminal's current directory.
PROJECT_ROOT = Path(__file__).resolve().parent.parent

# Folder containing our synthetic company documents.
DOCUMENTS_DIR = PROJECT_ROOT / "data" / "sample_documents"

# Fields every document must contain.
REQUIRED_FIELDS = {
    "id",
    "title",
    "department",
    "allowed_roles",
    "content",
}


def validate_document(document, filename):
    """Validate one document and return it if it is valid."""

    if not isinstance(document, dict):
        raise ValueError(f"{filename}: document must be a JSON object")

    missing_fields = REQUIRED_FIELDS - document.keys()
    if missing_fields:
        raise ValueError(
            f"{filename}: missing fields: {sorted(missing_fields)}"
        )

    # These fields must contain non-empty strings.
    for field in ("id", "title", "department", "content"):
        value = document[field]
        if not isinstance(value, str) or not value.strip():
            raise ValueError(
                f"{filename}: '{field}' must be a non-empty string"
            )

    # Access permissions must be a list of role names.
    roles = document["allowed_roles"]
    if (
        not isinstance(roles, list)
        or not roles
        or any(not isinstance(role, str) or not role.strip() for role in roles)
    ):
        raise ValueError(
            f"{filename}: 'allowed_roles' must be a non-empty list of strings"
        )

    return document


def load_documents(directory=DOCUMENTS_DIR):
    """Load, validate, and return all JSON documents in a directory."""

    directory = Path(directory)

    if not directory.is_dir():
        raise FileNotFoundError(
            f"Documents directory not found: {directory}"
        )

    documents = []
    seen_ids = set()

    for path in sorted(directory.glob("*.json")):
        try:
            with path.open("r", encoding="utf-8-sig") as file:
                document = json.load(file)
        except json.JSONDecodeError as error:
            raise ValueError(
                f"{path.name}: invalid JSON at line {error.lineno}, "
                f"column {error.colno}"
            ) from error

        document = validate_document(document, path.name)

        if document["id"] in seen_ids:
            raise ValueError(
                f"{path.name}: duplicate document ID '{document['id']}'"
            )

        seen_ids.add(document["id"])
        documents.append(document)

    return documents


if __name__ == "__main__":
    loaded_documents = load_documents()

    print(f"Successfully loaded {len(loaded_documents)} documents.")

    for document in loaded_documents:
        print(
            f"- {document['id']}: {document['title']} "
            f"(roles: {', '.join(document['allowed_roles'])})"
        )
