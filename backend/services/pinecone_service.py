from pinecone import Pinecone
from config import settings

# Initialize Database Connection
pc = Pinecone(api_key=settings.PINECONE_API_KEY)
index = pc.Index(settings.INDEX_NAME)

def search_pinecone(query_vector: list, crop_filter: str = "All"):
    """
    Database mein vectors search karta hai aur filter apply karta hai.
    """
    # 1. Base Search Setup (Top 3 paragraphs nikalne ke liye)
    search_params = {
        "vector": query_vector,
        "top_k": 3, 
        "include_metadata": True
    }
    
    # 🚀 2. THE TOKEN SAVING FILTER 
    # Agar user ne 'All' ke bajaye kisi specific crop ka naam select kiya hai
    if crop_filter and crop_filter != "All":
        # Note: Yeh assume karta hai ke aapki pdf ka naam "Rice_English.pdf" jaisa hai.
        # Aap apne mutabiq isko set kar sakti hain.
        expected_pdf_name = f"{crop_filter}_English.pdf"
        
        # Pinecone Metadata Filtering
        search_params["filter"] = {
            "source": {"$eq": expected_pdf_name}
        }
        print(f"🔍 FILTER ACTIVE: Searching strictly inside '{expected_pdf_name}'")
    else:
        print("🔍 FILTER OFF: Searching across all agricultural manuals.")
        
    # 3. Execute Search
    try:
        results = index.query(**search_params)
        
        # 4. Extract Text Content
        context = ""
        for match in results.get('matches', []):
            text = match['metadata'].get('text', '')
            context += text + "\n\n---\n\n"
            
        return context
    except Exception as e:
        print(f"❌ Pinecone Search Error: {e}")
        return ""