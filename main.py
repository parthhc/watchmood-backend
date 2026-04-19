from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from contextlib import asynccontextmanager

from src.db.sqlite import init_db
from src.db.reviews import add_review, get_all_reviews, update_review, delete_review
from src.db.movies import get_movie_by_tmdb_id, add_movie
from src.agents.recommendation_agent import get_recommendation
from src.agents.taste_agent import regenerate_taste_profile
from src.clients.tmdb import search_movies as tmdb_search, get_movie as tmdb_get_movie

@asynccontextmanager
async def lifespan(app: FastAPI):
    init_db()
    yield

app = FastAPI(lifespan=lifespan)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class RecommendationRequest(BaseModel):
    mood: str

class ReviewRequest(BaseModel):
    tmdb_id: int
    rating: float
    review_text: str

class ReviewUpdateRequest(BaseModel):
    rating: float
    review_text: str

@app.post("/recommend")
async def recommend(request: RecommendationRequest):
    try:
        recommendation = await get_recommendation(request.mood)
        return recommendation
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/reviews")
async def create_review(request: ReviewRequest):
    movie = get_movie_by_tmdb_id(request.tmdb_id)
    
    if not movie:
        tmdb_movie = tmdb_get_movie(request.tmdb_id)
        if not tmdb_movie:
            raise HTTPException(status_code=404, detail="Movie not found on TMDB")
        
        add_movie(
            tmdb_id=tmdb_movie["id"],
            title=tmdb_movie["title"],
            year=int(tmdb_movie["release_date"][:4]) if tmdb_movie.get("release_date") else 0,
            rating=tmdb_movie["vote_average"],
            overview=tmdb_movie["overview"],
            genres=str([g["id"] for g in tmdb_movie.get("genres", [])])
        )
        movie = get_movie_by_tmdb_id(request.tmdb_id)

    
    should_regenerate = add_review(
        tmdb_id=request.tmdb_id,
        title=movie["title"],
        rating=request.rating,
        review_text=request.review_text
    )

    if should_regenerate:
        await regenerate_taste_profile()

    return {"message": "Review added successfully"}

@app.get("/reviews")
def list_reviews():
    return get_all_reviews()

@app.put("/reviews/{review_id}")
async def edit_review(review_id: int, request: ReviewUpdateRequest):
    update_review(
        review_id=review_id,
        rating=request.rating,
        review_text=request.review_text
    )
    return {"message": "Review updated successfully"}

@app.delete("/reviews/{review_id}")
def remove_review(review_id: int):
    delete_review(review_id)
    return {"message": "Review deleted successfully"}


@app.get("/taste-profile")
def get_profile():
    from src.db.taste_profile import get_latest_taste_profile, get_profile_history
    profile = get_latest_taste_profile()
    if not profile:
        return {"profile": None, "history": []}
    return {
        "profile": profile.model_dump(),
        "history": get_profile_history()
    }

@app.post("/taste-profile/regenerate")
async def force_regenerate():
    profile = await regenerate_taste_profile()
    return profile.model_dump()

@app.get("/movies/search")
def search_movies(query: str):
    return tmdb_search(query)
