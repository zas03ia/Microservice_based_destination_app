import unittest
from unittest.mock import patch, MagicMock
from flask_jwt_extended import create_access_token
import os
import sys

import warnings

# Suppress deprecation warnings related to werkzeug
warnings.filterwarnings("ignore", category=DeprecationWarning)

# Dynamically construct the absolute path to the app module
current_dir = os.path.dirname(os.path.abspath(__file__))
project_root = os.path.abspath(os.path.join(current_dir, ".."))
sys.path.append(project_root)

from destination_service.app import app


class DestinationServiceTests(unittest.TestCase):
    def setUp(self):
        # Create Flask app and set testing mode
        self.app = app
        self.client = self.app.test_client()
        self.app.testing = True

        # Set up application context to use Flask-JWT-Extended
        with self.app.app_context():
            self.token = create_access_token(identity="1")

    @patch("destination_service.models.get_all_destinations")
    def test_list_destinations(self, mock_get_all_destinations):
        # Mock the get_all_destinations function
        mock_get_all_destinations.return_value = [
            {
                "id": 1,
                "name": "Paris",
                "description": "The City of Light",
                "location": "France",
            },
            {
                "id": 2,
                "name": "Tokyo",
                "description": "A bustling metropolis",
                "location": "Japan",
            },
        ]

        response = self.client.get(
            "/destinations/",
            headers={"Authorization": f"Bearer {self.token}"},
        )

        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            response.json,
            [
                {
                    "id": 1,
                    "name": "Paris",
                    "description": "The City of Light",
                    "location": "France",
                },
                {
                    "id": 2,
                    "name": "Tokyo",
                    "description": "A bustling metropolis",
                    "location": "Japan",
                },
            ],
        )

    # @patch("destination_service.utils.role_validation.requests.get")
    # @patch("destination_service.models.delete_destination")
    # def test_remove_destination_success(
    #     self, mock_delete_destination, mock_user_service
    # ):
    #     # Mock the user service to validate the role
    #     mock_user_service.return_value = MagicMock(
    #         status_code=200, json=lambda: {"role": "Admin"}
    #     )

    #     # Mock the delete_destination function
    #     mock_delete_destination.return_value = MagicMock(
    #         status_code=200, json={"message": "Destination deleted successfully."}
    #     )

    #     response = self.client.delete(
    #         "/destinations/1",
    #         headers={"Authorization": f"Bearer {self.token}"},
    #     )

    #     self.assertEqual(response.status_code, 200)
    #     self.assertEqual(response.json, {"message": "Destination 1 deleted."})

    # @patch("destination_service.utils.role_validation.requests.get")
    # @patch("destination_service.models.delete_destination")
    # def test_remove_destination_not_found(
    #     self, mock_delete_destination, mock_user_service
    # ):
    #     # Mock the user service to validate the role
    #     mock_user_service.return_value = MagicMock(
    #         status_code=200, json=lambda: {"role": "Admin"}
    #     )

    #     # Mock the delete_destination function for not found case
    #     mock_delete_destination.return_value = MagicMock(
    #         status_code=404, json={"error": "Destination with ID 1 not found."}
    #     )

    #     response = self.client.delete(
    #         "/destinations/1",
    #         headers={"Authorization": f"Bearer {self.token}"},
    #     )

    #     self.assertEqual(response.status_code, 404)
    #     self.assertEqual(response.json, {"error": "Destination with ID 1 not found."})

    # @patch("destination_service.utils.role_validation.requests.get")
    # def test_remove_destination_role_mismatch(self, mock_user_service):
    #     # Mock the user service to return a non-Admin role
    #     mock_user_service.return_value = MagicMock(
    #         status_code=200, json=lambda: {"role": "User"}
    #     )

    #     response = self.client.delete(
    #         "/destinations/1",
    #         headers={"Authorization": f"Bearer {self.token}"},
    #     )

    #     self.assertEqual(response.status_code, 403)
    #     self.assertEqual(response.json, {"valid": False})

    # @patch("destination_service.utils.role_validation.requests.get")
    # def test_remove_destination_user_not_found(self, mock_user_service):
    #     # Mock the user service to return user not found
    #     mock_user_service.return_value = MagicMock(status_code=404)

    #     response = self.client.delete(
    #         "/destinations/1",
    #         headers={"Authorization": f"Bearer {self.token}"},
    #     )

    #     self.assertEqual(response.status_code, 404)
    #     self.assertEqual(response.json, {"message": "User not found"})

    # @patch("destination_service.utils.role_validation.requests.get")
    # def test_remove_destination_auth_service_unavailable(self, mock_user_service):
    #     # Simulate an exception in the user service
    #     mock_user_service.side_effect = Exception("Service Unavailable")

    #     response = self.client.delete(
    #         "/destinations/1",
    #         headers={"Authorization": f"Bearer {self.token}"},
    #     )

    #     self.assertEqual(response.status_code, 503)
    #     self.assertEqual(response.json, {"message": "User Service unavailable"})


if __name__ == "__main__":
    unittest.main()
