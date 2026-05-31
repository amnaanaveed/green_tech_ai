from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from models.schemas import ChatRequest, ChatResponse
from services.llm_service import get_answer_from_ai

# Initialize FastAPI App
app = FastAPI(
    title="GreenTech AI API",
    description="Cross-lingual RAG Backend with Token Filters and LLM Fallback",
    version="1.0.0"
)

# CORS Middleware (React frontend ko allow karne ke liye)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], # Production mein isay apne Vercel URL se replace karenge
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Root Endpoint
@app.get("/")
def read_root():
    return {"message": "GreenTech AI Enterprise Server is Running! 🚀"}

# Main Chat Endpoint
@app.post("/chat", response_model=ChatResponse)
async def chat_endpoint(request: ChatRequest):
    """
    Frontend se sawal aur filters receive karta hai aur AI ka jawab return karta hai.
    """
    # LLM service ko request pass karein
    result = get_answer_from_ai(request)
    
    # Response schema ke mutabiq data wapis bhejein
    return ChatResponse(
        status="success",
        query=request.query,
        answer=result["answer"],
        ai_used=result["source_ai"]
    )