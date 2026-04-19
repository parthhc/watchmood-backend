import requests
import os
from dotenv import load_dotenv

load_dotenv()

TMDB_BASE_URL = "https://api.themoviedb.org/3"
HEADERS = {"Authorization": f"Bearer {os.getenv('TMDB_API_KEY')}"}

def get_movie(tmdb_id: int) -> dict:
    response = requests.get(
        f"{TMDB_BASE_URL}/movie/{tmdb_id}",
        headers=HEADERS
    )
    response.raise_for_status()
    return response.json()

def search_movies(query: str) -> list[dict]:
    response = requests.get(
        f"{TMDB_BASE_URL}/search/movie",
        headers=HEADERS,
        params={"query": query, "language": "en-US"}
    )
    response.raise_for_status()
    return response.json().get("results", [])

def fetch_movies_page(endpoint: str, page: int) -> list[dict]:
    response = requests.get(
        f"{TMDB_BASE_URL}{endpoint}",
        headers=HEADERS,
        params={"page": page, "language": "en-US"}
    )
    response.raise_for_status()
    return response.json().get("results", [])