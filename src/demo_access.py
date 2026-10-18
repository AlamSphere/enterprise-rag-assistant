
from src.document_loader import load_documents
from src.access_control import filter_documents


def main():
    documents = load_documents()

    for role in ("employee", "hr", "finance", "admin"):
        accessible = filter_documents(documents, role)

        print(f"\nRole: {role}")
        for document in accessible:
            print(f"- {document['title']}")


if __name__ == "__main__":
    main()
