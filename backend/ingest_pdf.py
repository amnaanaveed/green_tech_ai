import os
import PyPDF2
from sentence_transformers import SentenceTransformer
from pinecone import Pinecone, ServerlessSpec
from dotenv import load_dotenv

# ==========================================
# 1. CONFIGURATION & SETUP
# ==========================================
# Load environment variables from .env file
load_dotenv()

# Ab API Key direct code ke bajaye .env file se aayegi (100% secure)
PINECONE_API_KEY = os.getenv("PINECONE_API_KEY")

if not PINECONE_API_KEY:
    print("❌ ERROR: Pinecone API Key not found! Please check your .env file.")
    exit()

INDEX_NAME = "greentech-agri-db"
DATA_FOLDER = "data" # Yahan aapki 6 PDFs mojood hain

print("🚀 Starting GreenTech AI Data Ingestion Process...")

# Initialize Pinecone
pc = Pinecone(api_key=PINECONE_API_KEY)

# Create Index if it doesn't exist
if INDEX_NAME not in pc.list_indexes().names():
    print(f"Creating new Pinecone index: {INDEX_NAME}...")
    pc.create_index(
        name=INDEX_NAME,
        dimension=384, # all-MiniLM-L6-v2 hamesha 384 dimensions use karta hai
        metric="cosine",
        spec=ServerlessSpec(cloud="aws", region="us-east-1")
    )
    print("✅ Index created successfully!")

index = pc.Index(INDEX_NAME)

# Initialize HuggingFace Embedding Model
print("🧠 Loading HuggingFace Embedding Model (all-MiniLM-L6-v2)...")
model = SentenceTransformer("all-MiniLM-L6-v2")

# ==========================================
# 2. HELPER FUNCTIONS
# ==========================================
def extract_text_from_pdf(file_path):
    """PDF se text nikalne ka function"""
    text = ""
    try:
        with open(file_path, "rb") as file:
            reader = PyPDF2.PdfReader(file)
            for page in reader.pages:
                extracted = page.extract_text()
                if extracted:
                    text += extracted + " "
    except Exception as e:
        print(f"❌ Error reading {file_path}: {e}")
    return text

def chunk_text(text, chunk_size=150, overlap=20):
    """Text ko 150 words ke chunks mein todna (with 20 words overlap)"""
    words = text.split()
    chunks = []
    for i in range(0, len(words), chunk_size - overlap):
        chunk = " ".join(words[i:i + chunk_size])
        if len(chunk.split()) > 20: # Chote fazool chunks ko ignore karein
            chunks.append(chunk)
    return chunks

# ==========================================
# 3. MAIN PROCESSING LOOP
# ==========================================
all_vectors = []
vector_id_counter = 0

print(f"📂 Scanning '{DATA_FOLDER}' folder for PDFs...")

# Loop through all PDFs in the data folder
for filename in os.listdir(DATA_FOLDER):
    if filename.endswith(".pdf"):
        file_path = os.path.join(DATA_FOLDER, filename)
        print(f"\n📄 Processing: {filename}")
        
        # Step A: Extract Text
        raw_text = extract_text_from_pdf(file_path)
        print(f"  -> Extracted {len(raw_text)} characters.")
        
        # Step B: Make Chunks
        chunks = chunk_text(raw_text)
        print(f"  -> Created {len(chunks)} text chunks.")
        
        # Step C: Generate Embeddings and Prepare Vectors
        for chunk in chunks:
            # Generate embedding vector
            embedding = model.encode(chunk).tolist()
            
            # Prepare data format for Pinecone
            vector_data = {
                "id": f"vec_{filename}_{vector_id_counter}",
                "values": embedding,
                "metadata": {
                    "source": filename,
                    "text": chunk
                }
            }
            all_vectors.append(vector_data)
            vector_id_counter += 1

# ==========================================
# 4. UPLOAD TO PINECONE
# ==========================================
if len(all_vectors) > 0:
    print(f"\n⬆️ Uploading {len(all_vectors)} total vectors to Pinecone...")
    batch_size = 100 # Batching taake timeout na ho

    for i in range(0, len(all_vectors), batch_size):
        batch = all_vectors[i:i + batch_size]
        index.upsert(vectors=batch)
        print(f"  -> Uploaded batch {i//batch_size + 1}...")

    print("\n🎉 SUCCESS! All agricultural manuals have been embedded and uploaded to your Vector Database!")
else:
    print("\n⚠️ No data found to upload. Please check if your PDFs are in the 'data' folder.")