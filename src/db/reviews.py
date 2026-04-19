from src.db.sqlite import get_connection
from src.db.chroma import user_reviews

def add_review(tmdb_id: int, title: str, rating: float, review_text: str) -> bool:
    conn = get_connection()
    cursor = conn.cursor()
    
    cursor.execute("""
        INSERT INTO reviews (tmdb_id, rating, review_text)
        VALUES (?, ?, ?)
    """, (tmdb_id, rating, review_text))
    
    conn.commit()
    review_id = cursor.lastrowid
    conn.close()

    user_reviews.add(
        ids=[f"review_{review_id}"],
        documents=[f"{title}: {review_text}"],
        metadatas={
            "tmdb_id": str(tmdb_id),
            "title": title,
            "rating": rating,
        }
    )

    if get_review_count() % 5 == 0:
        return True  
    return False

def get_review_count() -> int:
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT COUNT(*) FROM reviews")
    count = cursor.fetchone()[0]
    conn.close()
    return count

def get_all_reviews() -> list[dict]:
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("""
        SELECT r.*, m.title FROM reviews r
        JOIN movies m ON r.tmdb_id = m.tmdb_id
        ORDER BY r.created_at DESC
    """)
    rows = cursor.fetchall()
    conn.close()
    return [dict(row) for row in rows]

def get_review_by_id(review_id: int) -> dict | None:
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("""
        SELECT r.*, m.title FROM reviews r
        JOIN movies m ON r.tmdb_id = m.tmdb_id
        WHERE r.id = ?
    """, (review_id,))
    row = cursor.fetchone()
    conn.close()
    return dict(row) if row else None

def get_review_by_tmdb_id(tmdb_id: int) -> list[dict]:
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("""
        SELECT r.*, m.title FROM reviews r
        JOIN movies m ON r.tmdb_id = m.tmdb_id
        WHERE r.tmdb_id = ?
        ORDER BY r.created_at DESC
    """, (tmdb_id,))
    rows = cursor.fetchall()
    conn.close()
    return [dict(row) for row in rows]

def update_review(review_id: int, rating: float, review_text: str):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("""
        UPDATE reviews SET rating = ?, review_text = ?
        WHERE id = ?
    """, (rating, review_text, review_id))
    conn.commit()
    conn.close()

    review = get_review_by_id(review_id)
    user_reviews.update(
        ids=[f"review_{review_id}"],
        documents=[f"{review['title']}: {review_text}"],
        metadatas={"rating": rating}
    )

def delete_review(review_id: int):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM reviews WHERE id = ?", (review_id,))
    conn.commit()
    conn.close()

    user_reviews.delete(ids=[f"review_{review_id}"])