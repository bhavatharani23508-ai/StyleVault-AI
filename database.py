import sqlite3
from datetime import datetime


DATABASE_NAME = "stylevault.db"


# =========================================================
# DATABASE CONNECTION
# =========================================================

def get_connection():

    connection = sqlite3.connect(
        DATABASE_NAME,
        check_same_thread=False
    )

    return connection


# =========================================================
# CREATE TABLE
# =========================================================

def initialize_database():

    connection = get_connection()

    cursor = connection.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS wardrobe (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            clothing_type TEXT,
            color TEXT,
            style TEXT,
            pattern TEXT,
            sleeve TEXT,
            confidence REAL,
            ocr_text TEXT,
            image_name TEXT,
            created_at TEXT
        )
    """)

    connection.commit()

    connection.close()


# =========================================================
# ADD CLOTHING
# =========================================================

def add_clothing(
    clothing_type,
    color,
    style,
    pattern,
    sleeve,
    confidence,
    ocr_text,
    image_name
):

    connection = get_connection()

    cursor = connection.cursor()

    cursor.execute("""
        INSERT INTO wardrobe (
            clothing_type,
            color,
            style,
            pattern,
            sleeve,
            confidence,
            ocr_text,
            image_name,
            created_at
        )
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
    """, (
        clothing_type,
        color,
        style,
        pattern,
        sleeve,
        confidence,
        ocr_text,
        image_name,
        datetime.now().strftime(
            "%Y-%m-%d %H:%M:%S"
        )
    ))

    connection.commit()

    connection.close()


# =========================================================
# GET ALL CLOTHING
# =========================================================

def get_all_clothing():

    connection = get_connection()

    cursor = connection.cursor()

    cursor.execute("""
        SELECT
            id,
            clothing_type,
            color,
            style,
            pattern,
            sleeve,
            confidence,
            ocr_text,
            image_name,
            created_at
        FROM wardrobe
        ORDER BY id DESC
    """)

    rows = cursor.fetchall()

    connection.close()

    return rows


# =========================================================
# DELETE CLOTHING
# =========================================================

def delete_clothing(item_id):

    connection = get_connection()

    cursor = connection.cursor()

    cursor.execute(
        """
        DELETE FROM wardrobe
        WHERE id = ?
        """,
        (item_id,)
    )

    connection.commit()

    connection.close()


# =========================================================
# COUNT CLOTHING
# =========================================================

def get_clothing_count():

    connection = get_connection()

    cursor = connection.cursor()

    cursor.execute(
        "SELECT COUNT(*) FROM wardrobe"
    )

    count = cursor.fetchone()[0]

    connection.close()

    return count