import requests
from functools import wraps
from flask import jsonify, request
from decouple import config


def validate_role(required_role):
    """Decorator to check if the user has the required role by calling the Auth Service."""

    def decorator(f):
        @wraps(f)
        def wrapped(*args, **kwargs):

            # Call the Auth Service to validate the role
            auth_service_url = f"{config('AUTH_SERVICE_URL')}/validate-role"
            payload = {"role": required_role}

            try:
                response = requests.post(
                    auth_service_url, json=payload, headers=request.headers
                )
                if response.status_code == 200 and response.json().get("valid"):
                    return f(*args, **kwargs)
                else:
                    return (
                        jsonify(
                            {
                                "message": "Forbidden: User does not have the required role"
                            }
                        ),
                        403,
                    )
            except requests.exceptions.RequestException as e:
                return jsonify({"message": "Auth Service unavailable"}), 503

        return wrapped

    return decorator
