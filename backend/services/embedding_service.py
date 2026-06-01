import google.generativeai as genai
from config import settings

# Configure Gemini API
genai.configure(api_key=settings.GEMINI_API_KEY)

print("🧠 Using Gemini Embeddings for Search...")

def get_query_embedding(query: str) -> list:
    """
    User query ko embedding vector mein convert karta hai.
    Lightweight hai aur Render free tier pe smoothly chalega.
    """

    try:
        response = genai.embed_content(
            model="models/embedding-001",
            content=query,
            task_type="retrieval_query"
        )

        return response["embedding"]

    except Exception as e:
        print(f"Embedding Error: {e}")
        return []