import sqlite3

DB_PATH = "./watchmood.db"

def get_connection():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row  # lets you access columns by name
    return conn

def init_db():
    conn = get_connection()
    cursor = conn.cursor()

    cursor.executescript("""
        CREATE TABLE IF NOT EXISTS movies (
            id INTEGER PRIMARY KEY,
            tmdb_id INTEGER UNIQUE NOT NULL,
            title TEXT NOT NULL,
            year INTEGER,
            rating REAL,
            overview TEXT,
            genres TEXT
        );

        CREATE TABLE IF NOT EXISTS reviews (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            tmdb_id INTEGER NOT NULL,
            rating REAL NOT NULL,
            review_text TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (tmdb_id) REFERENCES movies(tmdb_id)
        );

        CREATE TABLE IF NOT EXISTS taste_profile (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            profile_json TEXT NOT NULL,
            review_count INTEGER NOT NULL,  -- snapshot of how many reviews at generation time
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        );
    """)

    conn.commit()
    conn.close()

if __name__ == "__main__":
    init_db()
    print("DB initialized")