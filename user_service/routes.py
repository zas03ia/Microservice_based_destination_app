from flask import Blueprint, jsonify, request
from flask_jwt_extended import jwt_required, create_access_token, get_jwt_identity
from flasgger import swag_from
import os
from .models import (
    is_valid_email,
    create_user,
    get_user_by_email,
    validate_password,
    get_user_profile,
)
from .config import SWAGGER_DOCS_PATH

# Flask Blueprint for user routes
user_blueprint = Blueprint("users", __name__)


@user_blueprint.route("/register", methods=["POST"])
@swag_from(os.path.join(SWAGGER_DOCS_PATH, "register_user.yml"))
def register():
    """
    Register a new user.
    """
    data = request.get_json()
    required_fields = ["name", "email", "password", "role"]
    if not all(field in data for field in required_fields):
        return jsonify({"error": "Missing required fields"}), 400

    if not is_valid_email(data["email"]):
        return jsonify({"error": "Invalid email format"}), 400

    if data["role"] not in ["Admin", "User"]:
        return jsonify({"error": "Role must be 'Admin' or 'User'"}), 400

    if get_user_by_email(data["email"]):
        return jsonify({"error": "Email already exists"}), 400

    user = create_user(data["name"], data["email"], data["password"], data["role"])
    return jsonify({"message": "User registered successfully", "user": user}), 201


@user_blueprint.route("/login", methods=["POST"])
@swag_from(os.path.join(SWAGGER_DOCS_PATH, "login_user.yml"))
def login():
    """
    Authenticate a user and provide an access token.
    """
    data = request.get_json()
    if not data.get("email") or not data.get("password"):
        return jsonify({"error": "Email and password are required"}), 400

    if not is_valid_email(data["email"]):
        return jsonify({"error": "Invalid email format"}), 400

    user = validate_password(data["email"], data["password"])
    if not user:
        return jsonify({"error": "Invalid email or password"}), 401

    # Generate JWT token
    access_token = create_access_token(identity=user["id"])
    return jsonify({"message": "Login successful", "access_token": access_token}), 200


@user_blueprint.route("/profile", methods=["GET"])
@swag_from(os.path.join(SWAGGER_DOCS_PATH, "profile_user.yml"))
@jwt_required()
def profile():
    """
    View profile information (user-specific).
    """

    # Retrieve the user identity from the token
    current_user_id = get_jwt_identity()

    user = get_user_profile(current_user_id)
    if not user:
        return jsonify({"error": "User not found"}), 404

    return jsonify(user), 200
