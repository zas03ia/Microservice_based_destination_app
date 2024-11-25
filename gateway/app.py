from flask import Flask, jsonify, redirect
from gateway.config import Config
from gateway.routes import register_routes
from decouple import config

app = Flask(__name__)
app.config.from_object(Config)

# Register all routes
register_routes(app)


@app.route("/")
def home():
    """Home route."""
    return jsonify({"message": "Welcome to the Travel API Gateway!"})


@app.route("/docs/destination", methods=["GET"])
def destination_docs():
    return redirect(f"http://localhost:{config('DESTINATION_SERVICE_PORT')}/apidocs")


@app.route("/docs/user", methods=["GET"])
def user_docs():
    return redirect(f"http://localhost:{config('USER_SERVICE_PORT')}/apidocs")


@app.route("/docs/auth", methods=["GET"])
def auth_docs():
    return redirect(f"http://localhost:{config('AUTH_SERVICE_PORT')}/apidocs")


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=config("GATEWAY_SERVICE_PORT"), debug=Config.DEBUG)
