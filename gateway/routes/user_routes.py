from flask import request
from gateway.utils.request_handler import make_request
from gateway.config import Config
from flask import Blueprint

gateway_user_blueprint = Blueprint("gateway_user", __name__)


@gateway_user_blueprint.route("/register", methods=["POST"])
def register_user():
    """Register a new user."""
    return make_request("POST", f"{Config.USER_SERVICE_URL}/register", request.json)


@gateway_user_blueprint.route("/login", methods=["POST"])
def login_user():
    """Log in a user."""
    return make_request("POST", f"{Config.USER_SERVICE_URL}/login", request.json)


@gateway_user_blueprint.route("/profile", methods=["GET"])
def get_user_profile():
    """Get user profile."""
    return make_request("GET", f"{Config.USER_SERVICE_URL}/profile", request.json)
