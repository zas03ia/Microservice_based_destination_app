from gateway.utils.request_handler import make_request
from gateway.config import Config
from flask import Blueprint

gateway_destination_blueprint = Blueprint("gateway_destination", __name__)


@gateway_destination_blueprint.route("/", methods=["GET"])
def request_list_destinations():
    """Retrieve a list of all travel destinations."""
    return make_request("GET", Config.DESTINATION_SERVICE_URL)


@gateway_destination_blueprint.route("/<int:destination_id>", methods=["DELETE"])
def request_remove_destination(destination_id):
    """Delete a specific travel destination (Admin-only)."""
    return make_request("DELETE", f"{Config.DESTINATION_SERVICE_URL}/{destination_id}")
