import os
from pydantic_ai.models.google import GoogleModel
from pydantic_ai.providers.google import GoogleProvider
from dotenv import load_dotenv

load_dotenv()

provider = GoogleProvider(api_key=os.getenv('GEMINI_API_KEY'))
model = GoogleModel("gemini-2.0-flash-lite", provider=provider)

