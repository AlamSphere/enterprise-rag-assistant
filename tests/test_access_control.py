
import unittest

from src.access_control import filter_documents


class TestAccessControl(unittest.TestCase):
    def setUp(self):
        self.documents = [
            {
                "id": "public_handbook",
                "allowed_roles": ["employee", "hr", "finance", "admin"],
            },
            {
                "id": "hr_leave_policy",
                "allowed_roles": ["hr", "admin"],
            },
            {
                "id": "finance_expenses",
                "allowed_roles": ["finance", "admin"],
            },
        ]

    def test_employee_only_gets_public_document(self):
        result = filter_documents(self.documents, "employee")

        self.assertEqual(
            [doc["id"] for doc in result],
            ["public_handbook"],
        )

    def test_hr_gets_public_and_hr_documents(self):
        result = filter_documents(self.documents, "hr")
        ids = {doc["id"] for doc in result}

        self.assertEqual(ids, {"public_handbook", "hr_leave_policy"})

    def test_finance_cannot_access_hr_policy(self):
        result = filter_documents(self.documents, "finance")
        ids = {doc["id"] for doc in result}

        self.assertIn("finance_expenses", ids)
        self.assertNotIn("hr_leave_policy", ids)

    def test_admin_can_access_all_documents(self):
        result = filter_documents(self.documents, "admin")

        self.assertEqual(len(result), 3)

    def test_unknown_role_is_rejected(self):
        with self.assertRaises(ValueError):
            filter_documents(self.documents, "superuser")

    def test_missing_permissions_do_not_grant_access(self):
        documents = [{"id": "unconfigured_document"}]

        result = filter_documents(documents, "employee")

        self.assertEqual(result, [])


if __name__ == "__main__":
    unittest.main()
