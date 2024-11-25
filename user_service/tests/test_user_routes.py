import unittest
from unittest.mock import patch
from flask_jwt_extended import create_access_token
import os
import sys

# Dynamically construct the absolute path to the app module
current_dir = os.path.dirname(os.path.abspath(__file__))
project_root = os.path.abspath(os.path.join(current_dir, ".."))
sys.path.append(project_root)

from user_service.app import create_app


class UserServiceTests(unittest.TestCase):
    def setUp(self):
        # Create Flask app and set testing mode
        self.app = create_app()
        self.client = self.app.test_client()

        self.app.testing = True

        # Set up application context to use Flask-JWT-Extended
        with self.app.app_context():
            self.token = create_access_token(identity="1")

    @patch("user_service.models.get_user_by_email")
    def test_register_success_not(self, mock_get_user_by_email):
        # Mock the check for existing user
        mock_get_user_by_email.return_value = {"email": "john@example.com"}

        response = self.client.post(
            "/users/register",
            json={
                "name": "John Doe",
                "email": "john@example.com",
                "password": "password123",
                "role": "Admin",
            },
        )

        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json, {"error": "Email already exists"})

    @patch("user_service.models.get_user_by_email")
    def test_register_2(self, mock_get_user_by_email):
        # Mock the check for existing user
        mock_get_user_by_email.return_value = None

        response = self.client.post(
            "/users/register",
            json={
                "name": "John Doe",
                "email": "john@example.com",
                "password": "password123",
                "role": "Admin",
            },
        )

        self.assertEqual(response.status_code, 201)
        self.assertEqual(response.json["message"], "User registered successfully")
        self.assertEqual(response.json["user"]["email"], "john@example.com")


    @patch("user_service.models.validate_password")
    def test_login_invalid_credentials(self, mock_validate_password):
        # Mock the validate_password function to return None (invalid credentials)
        mock_validate_password.return_value = None

        response = self.client.post(
            "/users/login",
            json={"email": "john@example.com", "password": "wrongpassword"},
        )

        self.assertEqual(response.status_code, 401)
        self.assertEqual(response.json, {"error": "Invalid email or password"})

    
    @patch("user_service.models.get_user_profile")
    def test_profile_user_not_found(self, mock_get_user_profile):
        # Mock the get_user_profile function to return None (user not found)
        mock_get_user_profile.return_value = None

        response = self.client.get(
            "/users/profile", headers={"Authorization": f"Bearer {self.token}"}
        )

        self.assertEqual(response.status_code, 404)
        self.assertEqual(response.json, {"error": "User not found"})


if __name__ == "__main__":
    unittest.main()
