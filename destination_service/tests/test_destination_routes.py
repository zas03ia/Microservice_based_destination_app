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

    


if __name__ == "__main__":
    unittest.main()
