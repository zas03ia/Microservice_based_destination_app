from flask import Flask
from gateway.routes.destination_routes import gateway_destination_blueprint
from gateway.routes.user_routes import gateway_user_blueprint
from gateway.routes.auth_routes import gateway_auth_blueprint


def register_routes(app: Flask):
    """Registers all blueprints to the Flask app."""
    app.register_blueprint(gateway_destination_blueprint, url_prefix="/destinations")
    app.register_blueprint(gateway_user_blueprint, url_prefix="/users")
    app.register_blueprint(gateway_auth_blueprint, url_prefix="/auth")
