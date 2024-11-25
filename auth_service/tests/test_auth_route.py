import unittest
from unittest.mock import patch
from flask_jwt_extended import create_access_token
import os
import sys

# Dynamically construct the absolute path to the app module
current_dir = os.path.dirname(os.path.abspath(__file__))
project_root = os.path.abspath(os.path.join(current_dir, ".."))
sys.path.append(project_root)

from auth_service.app import app


class ValidateRoleTests(unittest.TestCase):
    def setUp(self):
        # Create Flask app and set testing mode
        self.app = app
        self.client = self.app.test_client()

        self.app.testing = True

        # Set up application context to use Flask-JWT-Extended
        with self.app.app_context():
            self.token = create_access_token(identity="1")

    @patch("requests.get")  # Mock the requests.get call
    def test_validate_role_success(self, mock_get):
        # Mock response from user service
        mock_get.return_value.status_code = 200
        mock_get.return_value.json.return_value = {"role": "admin"}

        response = self.client.post(
            "/auth/validate-role",
            headers={"Authorization": f"Bearer {self.token}"},
            json={"role": "admin"},
        )

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json, {"valid": True})

    @patch("requests.get")
    def test_validate_role_invalid_role(self, mock_get):
        # Mock response from user service
        mock_get.return_value.status_code = 200
        mock_get.return_value.json.return_value = {"role": "user"}

        response = self.client.post(
            "/auth/validate-role",
            headers={"Authorization": f"Bearer {self.token}"},
            json={"role": "admin"},
        )

        self.assertEqual(response.status_code, 403)
        self.assertEqual(response.json, {"valid": False})

    @patch("requests.get")
    def test_validate_role_missing_role(self, mock_get):
        response = self.client.post(
            "/auth/validate-role",
            headers={"Authorization": f"Bearer {self.token}"},
            json={},
        )

        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json, {"error": "Role is required"})

    @patch("requests.get")
    def test_validate_role_user_not_found(self, mock_get):
        # Mock response from user service
        mock_get.return_value.status_code = 404

        response = self.client.post(
            "/auth/validate-role",
            headers={"Authorization": f"Bearer {self.token}"},
            json={"role": "admin"},
        )

        self.assertEqual(response.status_code, 404)
        self.assertEqual(response.json, {"message": "User not found"})


if __name__ == "__main__":
    unittest.main()
