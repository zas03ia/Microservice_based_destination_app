import requests
from flask import jsonify

def make_request(method, url, data=None, headers=None):
    """Helper function to make HTTP requests."""
    try:
        response = requests.request(method, url, json=data, headers=headers)
        return jsonify(response.json()), response.status_code
    except requests.exceptions.RequestException as e:
        return jsonify({"error": str(e)}), 500
