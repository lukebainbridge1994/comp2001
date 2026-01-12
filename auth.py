import requests
from functools import wraps
from flask import request, jsonify

AUTH_API_URL = "https://web.socem.plymouth.ac.uk/COMP2001/auth/api/users"

# Hard-coded role mapping (allowed by coursework)
USER_ROLES = {
    "Grace Hopper": "admin",
    "Tim Berners-Lee": "user",
    "Ada Lovelace": "user"
}


def verify_credentials(username: str, password: str) -> bool:
    """
    Sends credentials to the Authenticator API.
    Returns True if verified, False otherwise.
    """
    payload = {
        "username": username,
        "password": password
    }

    try:
        response = requests.post(AUTH_API_URL, json=payload, timeout=5)
        response.raise_for_status()
        result = response.json()

        # Expected response: ["Verified", "False"]
        return isinstance(result, list) and result[0] == "Verified"

    except Exception:
        return False


def get_user_role(username: str) -> str:
    """
    Returns the role for a given user.
    Defaults to 'user' if not explicitly defined.
    """
    return USER_ROLES.get(username, "user")


def require_auth(required_role=None):
    """
    Decorator to protect endpoints with authentication
    and optional role-based access control.
    """
    def decorator(f):
        @wraps(f)
        def wrapper(*args, **kwargs):
            auth_data = request.get_json(silent=True)

            if not auth_data:
                return jsonify({"error": "Missing authentication data"}), 401

            username = auth_data.get("username")
            password = auth_data.get("password")

            if not username or not password:
                return jsonify({"error": "Username and password required"}), 401

            if not verify_credentials(username, password):
                return jsonify({"error": "Invalid credentials"}), 403

            role = get_user_role(username)

            if required_role and role != required_role:
                return jsonify({"error": "Forbidden"}), 403

            # Attach user info to request context
            request.user = {
                "username": username,
                "role": role
            }

            return f(*args, **kwargs)
        return wrapper
    return decorator
