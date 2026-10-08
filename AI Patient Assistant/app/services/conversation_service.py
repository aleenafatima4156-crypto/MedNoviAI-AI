
from app.database import get_connection


def add_message(
    conversation_id: str,
    role: str,
    content: str
):
    connection = get_connection()

    try:
        cursor = connection.cursor()

        cursor.execute(
            """
            INSERT OR IGNORE INTO conversations (conversation_id)
            VALUES (?)
            """,
            (conversation_id,)
        )

        cursor.execute(
            """
            INSERT INTO messages (conversation_id, role, content)
            VALUES (?, ?, ?)
            """,
            (conversation_id, role, content)
        )

        connection.commit()

    finally:
        connection.close()


def get_conversation(conversation_id: str) -> list[dict]:
    connection = get_connection()

    try:
        cursor = connection.cursor()

        cursor.execute(
            """
            SELECT role, content, created_at
            FROM messages
            WHERE conversation_id = ?
            ORDER BY id
            """,
            (conversation_id,)
        )

        rows = cursor.fetchall()

        return [
            {
                "role": row["role"],
                "content": row["content"],
                "created_at": row["created_at"]
            }
            for row in rows
        ]

    finally:
        connection.close()


def clear_conversation(conversation_id: str):
    connection = get_connection()

    try:
        cursor = connection.cursor()

        cursor.execute(
            "DELETE FROM messages WHERE conversation_id = ?",
            (conversation_id,)
        )

        cursor.execute(
            "DELETE FROM conversations WHERE conversation_id = ?",
            (conversation_id,)
        )

        connection.commit()

    finally:
        connection.close()