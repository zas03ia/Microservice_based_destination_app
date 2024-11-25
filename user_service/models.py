import re
from werkzeug.security import generate_password_hash, check_password_hash

# In-memory user storage
users = []


def is_valid_email(email):
    """Validate email format."""
    regex = r"[^@]+@[^@]+\.[^@]+"
    return re.match(regex, email) is not None


def create_user(name, email, password, role):
    """Create a new user."""
    hashed_password = generate_password_hash(password)
    user = {
        "id": str(len(users) + 1),
        "name": name,
        "email": email,
        "password": hashed_password,
        "role": role,
    }
    users.append(user)
    return user


def get_user_by_email(email):
    """Retrieve a user by email."""
    return next((user for user in users if user["email"] == email), None)


def validate_password(email, password):
    """Validate user credentials."""
    user = get_user_by_email(email)
    if user and check_password_hash(user["password"], password):
        return user
    return None


def get_user_profile(user_id):
    """Retrieve a user by ID."""
    return next((user for user in users if user["id"] == user_id), None)
