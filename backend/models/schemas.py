from pydantic import BaseModel
from typing import Optional

# 1. Frontend se aane wala Data (Request)
class ChatRequest(BaseModel):
    query: str
    
    # 🔥 Token Saving Filters (Optional fields)
    # Agar user koi specific crop select karta hai (e.g., "Rice"), toh LLM sirf usi PDF ko parhega
    crop_filter: Optional[str] = "All" 
    
    # Agar user ko chota jawab chahiye (e.g., "Short"), toh hum LLM ko tokens limit karne ka bolenge
    answer_length: Optional[str] = "Detailed" 

# 2. Backend se wapis jane wala Data (Response)
class ChatResponse(BaseModel):
    status: str
    query: str
    answer: str
    ai_used: str  # Yeh batayega ke jawab Gemini ne diya hai ya Groq nefrom pydantic import BaseModel
from typing import Optional

# 1. Frontend se aane wala Data (Request)
class ChatRequest(BaseModel):
    query: str
    
    # 🔥 Token Saving Filters (Optional fields)
    # Agar user koi specific crop select karta hai (e.g., "Rice"), toh LLM sirf usi PDF ko parhega
    crop_filter: Optional[str] = "All" 
    
    # Agar user ko chota jawab chahiye (e.g., "Short"), toh hum LLM ko tokens limit karne ka bolenge
    answer_length: Optional[str] = "Detailed" 

# 2. Backend se wapis jane wala Data (Response)
class ChatResponse(BaseModel):
    status: str
    query: str
    answer: str
    ai_used: str  