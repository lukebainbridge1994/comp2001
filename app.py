from flask import Flask, jsonify
from profile_repository import get_user_by_id

app = Flask(__name__)

@app.route("/")
def home():
    return jsonify({"message": "ProfileService is running"})

@app.route("/api/profile/me", methods=["GET"])
def get_my_profile():
    # TEMPORARY: hard-coded user for testing
    # This will be replaced by authentication
    
    user_id = 1

    profile = get_user_by_id(user_id)

    if not profile:
        return jsonify({"error": "User not found"}), 404

    return jsonify(profile)

if __name__ == "__main__":
    app.run(debug=True)
