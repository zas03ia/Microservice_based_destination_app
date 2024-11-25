from flask import Flask
from flask_jwt_extended import JWTManager
from auth_service.config import Config
from .routes import auth_blueprint
from flasgger import Swagger
from decouple import config


app = Flask(__name__)
app.config.from_object(Config)

# Initialize JWT Manager and Swagger
JWTManager(app)
Swagger(app)

# Register blueprints
app.register_blueprint(auth_blueprint, url_prefix="/auth")


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=config("AUTH_SERVICE_PORT"), debug=True)
