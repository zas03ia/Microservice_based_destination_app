from flask import Flask
from destination_service.routes import destination_blueprint
from destination_service.config import Config
from flasgger import Swagger
from flask_jwt_extended import JWTManager
from decouple import config



app = Flask(__name__)

# Configuration
app.config.from_object(Config)

# Initialize Swagger and JWT Manager
Swagger(app)
JWTManager(app)

# Register Blueprints
app.register_blueprint(destination_blueprint, url_prefix="/destinations")




if __name__ == "__main__":
    app.run(host="0.0.0.0", port=config("DESTINATION_SERVICE_PORT"), debug=True)
