import requests
from functools import wraps
from flask import request, jsonify

AUTH_API_URL = "https://web.socem.plymouth.ac.uk/COMP2001/auth/api/users"

ADMIN_USERS = [
    "Tim Berners-Lee"
]

# Verify credentials using the API
def verify_credentials(username: str, password: str) -> bool:
     
    payload = {
        "username": username,
        "password": password
    }

    try:
        response = requests.post(AUTH_API_URL, json=payload, timeout=5)
        response.raise_for_status()
        result = response.json()

        # Expected response: ["Verified", "True"/"False"]
        return isinstance(result, list) and result[0] == "Verified"

    except Exception:
        return False

# User role
def get_user_role(username: str) -> str:
    
    return "admin" if username in ADMIN_USERS else "user"


# Enforce authentication and optional role checks
def require_auth(required_role=None):
    
    def decorator(f):
        @wraps(f)
        def wrapper(*args, **kwargs):
            auth_data = request.get_json(silent=True)

            if not auth_data:
                return jsonify({"error": "Missing authentication data"}), 401

            # 'auth_username' instead of 'username' in the case
            # that the username is to be changed.
            username = auth_data.get("auth_username")
            password = auth_data.get("auth_password")

            if not username or not password:
                return jsonify({"error": "Username and password required"}), 401

            if not verify_credentials(username, password):
                return jsonify({"error": "Invalid credentials"}), 403

            role = get_user_role(username)

            if required_role and role != required_role:
                return jsonify({"error": "Forbidden"}), 403

            request.user = {
                "username": username,
                "role": role
            }

            return f(*args, **kwargs)
        return wrapper
    return decorator
