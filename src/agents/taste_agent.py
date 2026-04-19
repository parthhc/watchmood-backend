from pydantic_ai import Agent
from src.data_models import TasteProfile
from src.db.reviews import get_all_reviews
from src.db.taste_profile import save_taste_profile
from src.db.movies import get_movie_by_tmdb_id
from src.agents.model import model

taste_profile_agent = Agent(
    model=model,
    output_type=TasteProfile,
    system_prompt="""
    You are a movie taste analyst. Given a list of movie reviews and ratings, 
    synthesize a structured taste profile that captures the user's preferences.
    Be specific — avoid generic statements. Look for real patterns across the reviews.
    Please prioritize more recent reviews to generate taste profile, but also consider older reviews for a holistic view.

    You also have access to tools which allow you to get the full reviews as a dict and to fetch movie details by tmdb_id. Use these tools to get more context about the movies the user has reviewed, which can help you generate a more accurate taste profile.
    """
)

@taste_profile_agent.tool_plain
def get_all_reviews_as_dict() -> list[dict]:
    """
    This tool is used to fetch all of the user's reviews in a structured format.
            
    Here is the table used to create the reviews table to see what you have.
            CREATE TABLE IF NOT EXISTS reviews (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            tmdb_id INTEGER NOT NULL,
            rating REAL NOT NULL,
            review_text TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (tmdb_id) REFERENCES movies(tmdb_id)
        );

    """
    return get_all_reviews()

@taste_profile_agent
def get_movie_by_tmdb_id(tmdb_id: int) -> dict:
    """
    This tool is used to fetch movie details by tmdb_id. You can use this to get more context about the movies the user has reviewed, which can help you generate a more accurate taste profile.
    
    Args
     - tmdb_id: the TMDB ID of the movie to fetch details for.
    """
    return get_movie_by_tmdb_id(tmdb_id)

async def regenerate_taste_profile():
    reviews = get_all_reviews()
    reviews_text = "\n".join([
        f"{r['title']} — rated {r['rating']}/10: {r['review_text']}"
        for r in reviews
    ])
    result = await taste_profile_agent.run(
        f"Here are all the user's reviews:\n{reviews_text}"
    )
    save_taste_profile(result.output, review_count=len(reviews))
    return result.output