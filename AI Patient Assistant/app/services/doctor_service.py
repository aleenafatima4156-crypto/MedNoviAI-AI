from app.database import get_connection


def find_doctors_by_specialty(
    specialties: list[str]
) -> list[dict]:

    if not specialties:
        return []

    connection = get_connection()

    try:
        cursor = connection.cursor()

        placeholders = ",".join(
            "?" for _ in specialties
        )

        query = f"""
            SELECT
                id,
                name,
                specialty,
                experience_years,
                available
            FROM doctors
            WHERE specialty IN ({placeholders})
            AND available = 1
            ORDER BY experience_years DESC
        """

        cursor.execute(query, specialties)

        rows = cursor.fetchall()

        return [
            {
                "id": row["id"],
                "name": row["name"],
                "specialty": row["specialty"],
                "experience_years": row["experience_years"],
                "available": bool(row["available"])
            }
            for row in rows
        ]

    finally:
        connection.close()