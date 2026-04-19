# WatchMood backend

## Tech Stack

Pydantic AI — agent framework + structured outputs
ChromaDB — two collections (movie overviews, user reviews)
TMDB API — live ratings, metadata, search
FastAPI - Backend stuff

## Set Up Commands

1. Please have `uv` installed. See docs or use the following command

```
curl -LsSf https://astral.sh/uv/install.sh | sh
```

2. Set up your .env. Bring your own keys for TMDb and Gemini

```
cp .env.sample .env
```

3. Install deps

```
uv sync
```

4. Run DB seeder

```
uv run src/scripts/seed_movies.py
```

## Run command for the app

```
uvicorn main:app --reload
```
