from flask import Flask, jsonify, request
from profile_repository import (
    get_user_by_id,
    get_user_id_by_username,
    update_user_profile,
    delete_user
)
from auth import require_auth

app = Flask(__name__)


@app.route("/")
def home():
    return jsonify({"message": "ProfileService is running"})


@app.route("/api/profile/me", methods=["POST"])
@require_auth()
def get_my_profile():
    username = request.user["username"]

    user_id = get_user_id_by_username(username)
    if not user_id:
        return jsonify({"error": "User not found in ProfileService"}), 404

    profile = get_user_by_id(user_id)
    if not profile:
        return jsonify({"error": "Profile not found"}), 404

    return jsonify(serialise_profile(profile))

@app.route("/api/profile/me", methods=["PUT"])
@require_auth()
def update_my_profile():
    username = request.user["username"]
    updates = request.get_json()

    if not updates:
        return jsonify({"error": "No update data provided"}), 400

    user_id = get_user_id_by_username(username)
    if not user_id:
        return jsonify({"error": "User not found"}), 404

    current_profile = get_user_by_id(user_id)
    if not current_profile:
        return jsonify({"error": "Profile not found"}), 404

    merged_profile = {
        "username": updates.get("username", current_profile["username"]),
        "first_name": updates.get("first_name", current_profile["first_name"]),
        "last_name": updates.get("last_name", current_profile["last_name"]),
        "email": updates.get("email", current_profile["email"]),
        "phone_number": updates.get("phone_number", current_profile["phone_number"]),
        "date_of_birth": updates.get("date_of_birth") or current_profile["date_of_birth"],
        "height_cm": updates.get("height_cm", current_profile["height_cm"]),
        "weight_kg": updates.get("weight_kg", current_profile["weight_kg"]),
        "location": updates.get("location", current_profile["location"])
    }

    update_user_profile(user_id, merged_profile)

    return jsonify({"message": "Profile updated successfully"})

@app.route("/api/profile/me", methods=["DELETE"])
@require_auth()
def delete_my_profile():
    username = request.user["username"]

    user_id = get_user_id_by_username(username)
    if not user_id:
        return jsonify({"error": "User not found"}), 404

    delete_user(user_id)

    return jsonify({"message": "Profile deleted successfully"})

# To prevent showing the time, just the date 
def serialise_profile(profile: dict):
    return {
        **profile,
        "date_of_birth": (
            profile["date_of_birth"].isoformat()
            if profile.get("date_of_birth")
            else None
        )
    }

print(app.url_map)

if __name__ == "__main__":
    app.run(debug=True)
