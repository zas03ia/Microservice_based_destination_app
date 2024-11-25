from flask import Blueprint, request
from gateway.utils.request_handler import make_request
from gateway.config import Config

gateway_auth_blueprint = Blueprint("gateway_auth", __name__)


@gateway_auth_blueprint.route("/validate-role", methods=["POST"])
def validate_user_role():
    """Validate user role by forwarding request to the auth service."""
    # Forward the request to the auth service validate-role route
    return make_request(
        "POST", f"{Config.AUTH_SERVICE_URL}/validate-role", request.json
    )
