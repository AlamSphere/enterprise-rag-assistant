
import json
import tempfile
import unittest
from pathlib import Path

from src.document_loader import load_documents


class TestDocumentLoader(unittest.TestCase):
    def setUp(self):
        # Create a temporary folder for each test.
        self.temp_dir = tempfile.TemporaryDirectory()
        self.directory = Path(self.temp_dir.name)

        # A valid example document used by our tests.
        self.valid_document = {
            "id": "test_document",
            "title": "Test Document",
            "department": "public",
            "allowed_roles": ["employee"],
            "content": "This is test content.",
        }

    def tearDown(self):
        # Remove the temporary folder after each test.
        self.temp_dir.cleanup()

    def write_json(self, filename, data):
        """Write a JSON document into the temporary folder."""
        path = self.directory / filename

        with path.open("w", encoding="utf-8") as file:
            json.dump(data, file)

        return path

    def test_load_valid_document(self):
        self.write_json("valid.json", self.valid_document)

        documents = load_documents(self.directory)

        self.assertEqual(len(documents), 1)
        self.assertEqual(documents[0]["id"], "test_document")

    def test_reject_missing_required_field(self):
        invalid_document = self.valid_document.copy()
        del invalid_document["title"]

        self.write_json("missing_title.json", invalid_document)

        with self.assertRaisesRegex(ValueError, "missing fields"):
            load_documents(self.directory)

    def test_reject_malformed_json(self):
        path = self.directory / "broken.json"
        path.write_text('{"id": "broken",', encoding="utf-8")

        with self.assertRaisesRegex(ValueError, "invalid JSON"):
            load_documents(self.directory)

    def test_reject_duplicate_document_ids(self):
        self.write_json("first.json", self.valid_document)

        second_document = self.valid_document.copy()
        second_document["title"] = "Another Document"
        self.write_json("second.json", second_document)

        with self.assertRaisesRegex(ValueError, "duplicate document ID"):
            load_documents(self.directory)


if __name__ == "__main__":
    unittest.main()
