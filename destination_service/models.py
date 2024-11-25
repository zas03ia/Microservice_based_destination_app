from typing import List, Dict
from flask import jsonify, make_response, Response

# In-memory storage for simplicity
destinations = [
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


def get_all_destinations() -> List[Dict]:
    """
    Retrieve all destinations.
    :return: List of all destination dictionaries.
    """
    return destinations


def delete_destination(destination_id: int) -> Response:
    """
    Delete a destination by its ID.
    :param destination_id: The ID of the destination to delete.
    :return: A Flask response object with a status code indicating success or error.
    """
    global destinations
    initial_count = len(destinations)

    destinations = [d for d in destinations if d["id"] != destination_id]

    if len(destinations) < initial_count:
        # Return a 200 OK response on successful deletion
        return make_response(
            jsonify({"message": "Destination deleted successfully."}), 200
        )

    # Return a 404 Not Found response if the destination does not exist
    return make_response(
        jsonify({"error": f"Destination with ID {destination_id} not found."}), 404
    )
