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
        "date_of_birth": str(row.DateOfBirth) if row.DateOfBirth else None,
        "height_cm": row.Height_cm,
        "weight_kg": row.Weight_kg,
        "location": row.Location
    }