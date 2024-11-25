from flask import Flask
from .routes import user_blueprint
from user_service.config import Config
from flasgger import Swagger
from flask_jwt_extended import JWTManager
from decouple import config


def create_app():
    app = Flask(__name__)

    # Configuration
    app.config.from_object(Config)

    # Initialize Swagger and JWT Manager
    Swagger(app)
    JWTManager(app)

    # Register Blueprints
    app.register_blueprint(user_blueprint, url_prefix="/users")

    return app


if __name__ == "__main__":
    app = create_app()
    app.run(host="0.0.0.0", port=config("USER_SERVICE_PORT"), debug=True)
