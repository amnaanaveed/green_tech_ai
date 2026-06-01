import google.generativeai as genai
from config import settings

# Configure Gemini API
genai.configure(api_key=settings.GEMINI_API_KEY)

print("🧠 Using Gemini Embedding Model for Search...")

def get_query_embedding(query: str) -> list:
    """
    User ke text question ko embedding vector mein convert karta hai.
    Lightweight hai aur Render free tier pe easily chalega.
    """

    response = genai.embed_content(
        model="models/text-embedding-004",
        content=query,
        task_type="retrieval_query"
    )

    return response["embedding"]