from db import get_connection


def get_user_by_id(user_id: int):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute(
        "EXEC CW2.UserAccountRead @UserID = ?",
        user_id
    )

    row = cursor.fetchone()
    conn.close()

    if not row:
        return None

    return {
        "user_id": row.UserID,
        "username": row.Username,
        "first_name": row.FirstName,
        "last_name": row.LastName,
        "email": row.Email,
        "phone_number": row.PhoneNumber,
        "date_of_birth": row.DateOfBirth,
        "height_cm": row.Height_cm,
        "weight_kg": row.Weight_kg,
        "location": row.Location
    }


def get_user_id_by_username(username: str):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute(
        "SELECT UserID FROM CW2.UserAccount WHERE Username = ?",
        username
    )

    row = cursor.fetchone()
    conn.close()

    return row.UserID if row else None

def update_user_profile(user_id: int, data: dict):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute(
        "EXEC CW2.UserAccountUpdate ?, ?, ?, ?, ?, ?, ?, ?, ?, ?",
        user_id,
        data["username"],
        data["first_name"],
        data["last_name"],
        data["email"],
        data["phone_number"],
        data["date_of_birth"],
        data["height_cm"],
        data["weight_kg"],
        data["location"]
    )

    conn.commit()
    conn.close()

def delete_user(user_id: int):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute(
        "EXEC CW2.UserAccountDelete ?",
        user_id
    )

    conn.commit()
    conn.close()
