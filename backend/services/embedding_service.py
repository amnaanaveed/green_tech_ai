from sentence_transformers import SentenceTransformer
from config import settings

print("🧠 Loading HuggingFace Model for Search...")
# Load the model once when the server starts to save time
embedding_model = SentenceTransformer(settings.EMBEDDING_MODEL)

def get_query_embedding(query: str) -> list:
    """
    User ke text sawal ko 384-dimensional vector mein convert karta hai.
    """
    # Generate and return the vector as a Python list
    return embedding_model.encode(query).tolist()