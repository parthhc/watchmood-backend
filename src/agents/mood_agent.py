from src.data_models import MoodQuery
from src.agents.model import model
from pydantic_ai import Agent

mood_agent = Agent(
    model=model,
    output_type=MoodQuery,
    system_prompt="""
    You are a movie mood interpreter. Convert vague mood descriptions into structured search parameters.
    Be generous with themes and genres — cast a wide net so the recommendation agent has good candidates to work with.

    Make sure the mood query prioritzes the query over the taste profile.
    For example, users who hate horror are still likely to ask for a horror movie due to them being in a different context.
    That being said, do not ignore the taste profile whatsoever.
    """
)

async def interpret_mood(raw_input: str, taste_profile) -> MoodQuery:
    profile_context = taste_profile.model_dump_json() if taste_profile else "No profile yet"
    result = await mood_agent.run(
        f"Mood: {raw_input}\nUser taste profile: {profile_context}"
    )
    return result.output
