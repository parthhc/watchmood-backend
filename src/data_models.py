from pydantic import BaseModel

class TasteProfile(BaseModel):
    preferred_genres: list[str]
    preferred_pacing: str  # e.g. "slow burn", "fast-paced"
    favorite_themes: list[str]
    disliked_elements: list[str]
    preferred_era: str  # e.g. "90s-2000s", "modern"
    notable_favorites: list[str]  # specific movies

class MoodQuery(BaseModel):
    raw_input: str
    interpreted_genres: list[str]
    interpreted_themes: list[str]
    desired_pacing: str
    conflict_with_profile: bool
    conflict_note: str | None

class Recommendation(BaseModel):
    title: str
    year: int
    rating: float
    reasoning: str
    conflict_note: str | None  # populated if mood diverged from profile