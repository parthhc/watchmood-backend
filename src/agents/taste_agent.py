from pydantic_ai import Agent
from src.data_models import TasteProfile
from src.db.reviews import get_all_reviews
from src.db.taste_profile import save_taste_profile
from src.agents.model import model

taste_profile_agent = Agent(
    model=model,
    output_type=TasteProfile,
    system_prompt="""
    You are a movie taste analyst. Given a list of movie reviews and ratings, 
    synthesize a structured taste profile that captures the user's preferences.
    Be specific — avoid generic statements. Look for real patterns across the reviews.
    """
)

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