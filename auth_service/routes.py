import requests
from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from flasgger import swag_from
from .config import SWAGGER_DOCS_PATH
from decouple import config
import os

auth_blueprint = Blueprint("auth", __name__)


@auth_blueprint.route("/validate-role", methods=["POST"])
@swag_from(os.path.join(SWAGGER_DOCS_PATH, "validate_role.yml"))
@jwt_required()
def validate_role_service():
    """
    Check if the current user has the required role.
    """

    # Parse the required role from the request JSON payload
    data = request.get_json()
    required_role = data.get("role")

    if not required_role:
        return jsonify({"error": "Role is required"}), 400

    # Get the current user information from user service
    user_service_url = f"{config('USER_SERVICE_URL')}/profile"

    try:
        response = requests.get(user_service_url, headers=request.headers)
        if response.status_code == 200:
            # Validate the user's role
            is_valid = required_role == response.json().get("role")
            return (
                jsonify({"valid": is_valid}),
                200 if is_valid else 403,
            )
        else:
            return (
                jsonify({"message": "User not found"}),
                404,
            )
    except requests.exceptions.RequestException as e:
        return jsonify({"message": "User Service unavailable"}), 503
