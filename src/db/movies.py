from src.db.sqlite import get_connection
from src.db.chroma import movie_overviews

def add_movie(tmdb_id: int, title: str, year: int, rating: float, overview: str, genres: str):
    conn = get_connection()
    cursor = conn.cursor()
    
    existing = movie_overviews.get(ids=[str(tmdb_id)])

    if existing["ids"]: return

    cursor.execute("""
        INSERT OR IGNORE INTO movies (tmdb_id, title, year, rating, overview, genres)
        VALUES (?, ?, ?, ?, ?, ?)
    """, (tmdb_id, title, year, rating, overview, genres))
    conn.commit()
    conn.close()

    # sync to chromadb
    movie_overviews.add(
        ids=[str(tmdb_id)],
        documents=[overview],  # overview is what gets embedded + queried by mood
        metadatas=[{
            "tmdb_id": str(tmdb_id),
            "title": title,
            "year": year,
            "rating": rating,
            "genres": genres
        }]
    )

def get_movie_by_tmdb_id(tmdb_id: int):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM movies WHERE tmdb_id = ?", (tmdb_id,))
    row = cursor.fetchone()
    conn.close()
    return dict(row) if row else None

def get_all_movies():
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM movies")
    rows = cursor.fetchall()
    conn.close()
    return [dict(row) for row in rows]