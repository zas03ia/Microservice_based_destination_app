from flask import Blueprint, jsonify
from flask_jwt_extended import jwt_required
from destination_service.utils.role_validation import validate_role
from destination_service.models import get_all_destinations, delete_destination
from flasgger import swag_from
import os
from .config import SWAGGER_DOCS_PATH

destination_blueprint = Blueprint("destinations", __name__)


@destination_blueprint.route("/", methods=["GET"])
@swag_from(os.path.join(SWAGGER_DOCS_PATH, "list_destinations.yml"))
@jwt_required()
def list_destinations():
    """Retrieve a list of all travel destinations."""
    destinations = get_all_destinations()
    return jsonify(destinations), 200


@destination_blueprint.route("/<int:destination_id>", methods=["DELETE"])
@swag_from(os.path.join(SWAGGER_DOCS_PATH, "delete_destination.yml"))
@jwt_required()
@validate_role("Admin")
def remove_destination(destination_id):
    """Delete a specific travel destination (Admin-only)."""
    delete_destination(destination_id)
    return jsonify({"message": f"Destination {destination_id} deleted."}), 200
