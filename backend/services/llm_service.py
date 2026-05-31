import os
# 🔥 Python 3.14 Protobuf Crash Bypass
os.environ["PROTOCOL_BUFFERS_PYTHON_IMPLEMENTATION"] = "python"

import warnings
warnings.filterwarnings("ignore")

import google.generativeai as genai
from groq import Groq
from config import settings
from models.schemas import ChatRequest
from services.embedding_service import get_query_embedding
from services.pinecone_service import search_pinecone

# ==========================================
# 1. INITIALIZE AI CLIENTS
# ==========================================
# Initialize Gemini (Stable SDK)
genai.configure(api_key=settings.GEMINI_API_KEY)
gemini_model = genai.GenerativeModel(settings.GEMINI_MODEL)

# Initialize Groq (Fallback AI)
groq_client = Groq(api_key=settings.GROQ_API_KEY)

# ==========================================
# 2. THE CORE RAG & FALLBACK LOGIC
# ==========================================
def get_answer_from_ai(request: ChatRequest) -> dict:
    try:
        # STEP 1: Convert User Query to Vector
        query_embedding = get_query_embedding(request.query)
        
        # STEP 2: Search Pinecone (Token Saving Filter applied here via crop_filter)
        context = search_pinecone(query_embedding, request.crop_filter)
        
        # STEP 3: Handle Answer Length Filter
        length_instruction = ""
        if request.answer_length == "Short":
            length_instruction = "Give a very brief, to-the-point answer (Maximum 2-3 sentences). Do not waste tokens."
        else:
            length_instruction = "Explain the solution in detail, step-by-step."

        # STEP 4: The Updated "Smart & Flexible" System Prompt
        # STEP 4: The FORCEFUL "Smart & Flexible" System Prompt
        prompt = f"""
        You are 'GreenTech AI', an expert agricultural assistant for farmers in Pakistan.
        
        Context from Manuals:
        {context}
        
        User Query: {request.query}
        
        CRITICAL INSTRUCTIONS:
        1. First, try to answer using the 'Context from Manuals'.
        2. IF the context does not contain the exact answer, YOU MUST USE YOUR OWN GENERAL KNOWLEDGE to provide a solution. NEVER say "I don't know", "I don't have information in the manuals", or apologize. Just confidently give a helpful answer.
        3. LANGUAGE RULE: DETECT the exact language/script of the User Query. You MUST reply in the exact same language and script (e.g., Roman Urdu query = Roman Urdu reply).
        4. Make the answer practical for a farmer.
        5. {length_instruction}
        """

        # STEP 5: PRIMARY AI (Try Gemini First)
        try:
            print("🤖 Attempting to generate answer using GEMINI...")
            response = gemini_model.generate_content(prompt)
            return {"answer": response.text, "source_ai": "Gemini 2.5 Flash"}
            
        except Exception as gemini_error:
            # Yahan par Fallback Logic Trigger Hota hai!
            print(f"⚠️ Gemini Failed (Limit/Error): {gemini_error}")
            print("🔄 Switching to GROQ Fallback...")
            
            # STEP 6: FALLBACK AI (If Gemini fails, use Groq Llama 3)
            chat_completion = groq_client.chat.completions.create(
                messages=[
                    {"role": "user", "content": prompt}
                ],
                model="llama3-70b-8192", 
                temperature=0.5,
            )
            return {"answer": chat_completion.choices[0].message.content, "source_ai": "Groq Llama-3"}

    except Exception as e:
        return {"answer": f"System Error: {str(e)}", "source_ai": "None"}