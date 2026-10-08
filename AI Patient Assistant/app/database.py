import sqlite3
from pathlib import Path


BASE_DIR = Path(__file__).resolve().parent.parent
DATA_DIR = BASE_DIR / "data"

DATA_DIR.mkdir(exist_ok=True)

DATABASE_PATH = DATA_DIR / "patient_assistant.db"


def get_connection():
    connection = sqlite3.connect(DATABASE_PATH)
    connection.row_factory = sqlite3.Row
    return connection


def initialize_database():

    connection = get_connection()

    cursor = connection.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS conversations (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            conversation_id TEXT UNIQUE NOT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """)

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS messages (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            conversation_id TEXT NOT NULL,
            role TEXT NOT NULL,
            content TEXT NOT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """)

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS doctors (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            specialty TEXT NOT NULL,
            experience_years INTEGER DEFAULT 0,
            available INTEGER DEFAULT 1
        )
    """)

    connection.commit()
    connection.close()

def seed_doctors():
    doctors = [
        ("Dr. Ahmed Khan", "Cardiology", 12),
        ("Dr. Sara Ali", "Neurology", 8),
        ("Dr. Hina Malik", "Dermatology", 10),
        ("Dr. Usman Raza", "Gastroenterology", 9),
        ("Dr. Ayesha Noor", "ENT", 7),
        ("Dr. Hamza Shah", "Orthopedics", 11),
        ("Dr. Bilal Ahmed", "Pulmonology", 13),
        ("Dr. Fatima Zahra", "General Medicine", 6),
    ]

    connection = get_connection()

    try:
        cursor = connection.cursor()

        for name, specialty, experience in doctors:
            cursor.execute(
                """
                INSERT OR IGNORE INTO doctors
                (name, specialty, experience_years, available)
                VALUES (?, ?, ?, 1)
                """,
                (name, specialty, experience)
            )

        connection.commit()

    finally:
        connection.close()