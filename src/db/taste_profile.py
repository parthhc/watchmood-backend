import json
from src.db.sqlite import get_connection
from src.data_models import TasteProfile

def save_taste_profile(profile: TasteProfile, review_count: int):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("""
        INSERT INTO taste_profile (profile_json, review_count)
        VALUES (?, ?)
    """, (profile.model_dump_json(), review_count))
    conn.commit()
    conn.close()

def get_latest_taste_profile() -> TasteProfile | None:
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("""
        SELECT profile_json FROM taste_profile
        ORDER BY created_at DESC
        LIMIT 1
    """)
    row = cursor.fetchone()
    conn.close()
    return TasteProfile.model_validate_json(row["profile_json"]) if row else None

def get_profile_history() -> list[dict]:
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("""
        SELECT review_count, created_at FROM taste_profile
        ORDER BY created_at DESC
    """)
    rows = cursor.fetchall()
    conn.close()
    return [dict(row) for row in rows]