import os
from dotenv import load_dotenv

# Load variables from .env file
load_dotenv()

class Settings:
    # 🔑 API Keys
    PINECONE_API_KEY = os.getenv("PINECONE_API_KEY")
    GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
    GROQ_API_KEY = os.getenv("GROQ_API_KEY")
    
    # 🗄️ Database Info
    INDEX_NAME = "greentech-agri-db"
    
    # 🧠 AI Models
    EMBEDDING_MODEL = "all-MiniLM-L6-v2"
    GEMINI_MODEL = "gemini-2.5-flash"

# Create an instance to use everywhere
settings = Settings()

if not settings.PINECONE_API_KEY:
    print("⚠️ WARNING: API Keys are missing in .env file!")