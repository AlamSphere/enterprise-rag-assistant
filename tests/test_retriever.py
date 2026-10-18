
import unittest

from src.retriever import search_documents


class TestRetriever(unittest.TestCase):
    def test_hr_can_find_leave_policy(self):
        results = search_documents(
            "How much annual leave do employees receive?",
            "hr",
        )

        self.assertTrue(results)
        self.assertTrue(
            any(result["document_id"] == "hr_leave_policy" for result in results)
        )

    def test_employee_cannot_retrieve_hr_policy(self):
        results = search_documents(
            "How much annual leave do employees receive?",
            "employee",
        )

        self.assertFalse(
            any(result["document_id"] == "hr_leave_policy" for result in results)
        )

    def test_empty_query_is_rejected(self):
        with self.assertRaises(ValueError):
            search_documents("", "employee")


if __name__ == "__main__":
    unittest.main()
