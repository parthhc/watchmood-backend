import chromadb
import google.generativeai as genai
from chromadb import Documents, EmbeddingFunction, Embeddings
from dotenv import load_dotenv
import os

load_dotenv()
genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

class GeminiEmbeddingFunction(EmbeddingFunction):
    def __call__(self, input: Documents) -> Embeddings:
        result = genai.embed_content(
            model="models/gemini-embedding-001",
            content=input
        )
        return result["embedding"]

client = chromadb.PersistentClient(path="./chroma_store")
embedding_fn = GeminiEmbeddingFunction()

movie_overviews = client.get_or_create_collection(
    name="movie_overviews",
    embedding_function=embedding_fn
)

user_reviews = client.get_or_create_collection(
    name="user_reviews",
    embedding_function=embedding_fn
)