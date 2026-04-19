import requests
import os
import sys
import time
from dotenv import load_dotenv

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../../")))
from src.db.sqlite import init_db
from src.db.movies import add_movie

load_dotenv()

TMDB_API_KEY = os.getenv("TMDB_API_KEY")
TMDB_BASE_URL = "https://api.themoviedb.org/3"
HEADERS = {"Authorization": f"Bearer {TMDB_API_KEY}"}

def fetch_movies(endpoint: str, total_pages: int) -> list[dict]:
    movies = []
    for page in range(1, total_pages + 1):
        print(f"Fetching {endpoint} page {page}/{total_pages}...")
        response = requests.get(
            f"{TMDB_BASE_URL}{endpoint}",
            headers=HEADERS,
            params={"page": page, "language": "en-US"}
        )
        if response.status_code != 200:
            print(f"Failed on page {page}: {response.status_code}")
            continue
        movies.extend(response.json().get("results", []))
    return movies

def seed():
    init_db()

    all_movies = []
    seen_ids = set()

    endpoints = [
        ("/movie/popular", 8),
        ("/movie/top_rated", 8),
        ("/movie/now_playing", 4),
    ]

    for endpoint, pages in endpoints:
        movies = fetch_movies(endpoint, pages)
        for movie in movies:
            if movie["id"] not in seen_ids and movie.get("overview"):
                seen_ids.add(movie["id"])
                all_movies.append(movie)

    print(f"\nSeeding {len(all_movies)} unique movies...")

    for i, movie in enumerate(all_movies):
        try:
            add_movie(
                tmdb_id=movie["id"],
                title=movie["title"],
                year=int(movie["release_date"][:4]) if movie.get("release_date") else 0,
                rating=movie["vote_average"],
                overview=movie["overview"],
                genres=str(movie["genre_ids"])
            )
            print(f"[{i+1}/{len(all_movies)}] Added: {movie['title']}")
            time.sleep(3)
        except Exception as e:
            print(f"Failed to add {movie['title']}: {e}")
            continue

    print("\nDone seeding!")

if __name__ == "__main__":
    seed()