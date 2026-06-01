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

# CORS Middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "*"
        # Production mein:
        # "https://your-vercel-app.vercel.app"
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Root Endpoint
@app.get("/")
def read_root():
    return {
        "message": "GreenTech AI Enterprise Server is Running! 🚀"
    }

# Main Chat Endpoint
@app.post("/chat", response_model=ChatResponse)
async def chat_endpoint(request: ChatRequest):

    try:
        # AI response generate karo
        result = get_answer_from_ai(request)

        return ChatResponse(
            status="success",
            query=request.query,
            answer=result["answer"],
            ai_used=result["source_ai"]
        )

    except Exception as e:

        return ChatResponse(
            status="error",
            query=request.query,
            answer=f"System Error: {str(e)}",
            ai_used="None"
        )