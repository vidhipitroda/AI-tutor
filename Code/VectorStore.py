"""
Build and save FAISS vector store from cached chunks.
Embeds all 6,694 chunks using OpenAI's embedding model.
Saves FAISS index to disk for fast retrieval.
"""
import os
import pickle
import time
from dotenv import load_dotenv
from langchain_openai import OpenAIEmbeddings
from langchain_community.vectorstores import FAISS
from langchain_core.documents import Document

# Load .env file
load_dotenv()

# -----------------------------------------------------------------------
# CONFIG
# -----------------------------------------------------------------------
BASE_DIR = "/Users/vidhipitroda/Desktop/Projects/AI tutor"
CACHE_FILE = os.path.join(BASE_DIR, "Data/chunks_cache.pkl")
FAISS_INDEX_PATH = os.path.join(BASE_DIR, "Data/faiss_index")
EMBEDDING_MODEL = "text-embedding-3-small"  # Fast & cheap

print("=" * 70)
print("FAISS Vector Store Builder")
print("=" * 70)

# -----------------------------------------------------------------------
# 1. Load chunks
# -----------------------------------------------------------------------
print("\n[1/3] Loading chunks from cache...")
if not os.path.exists(CACHE_FILE):
    print(f"ERROR: Cache file not found at {CACHE_FILE}")
    print("Run Ingestion.py first to build the cache.")
    exit(1)

with open(CACHE_FILE, "rb") as f:
    chunks = pickle.load(f)

print(f"✅ Loaded {len(chunks)} chunks")
if len(chunks) == 0:
    print("ERROR: Cache is empty!")
    exit(1)

# -----------------------------------------------------------------------
# 2. Initialize embeddings
# -----------------------------------------------------------------------
print(f"\n[2/3] Initializing OpenAI embeddings (model: {EMBEDDING_MODEL})...")
try:
    embeddings = OpenAIEmbeddings(model=EMBEDDING_MODEL)
    print("✅ Embeddings initialized")
except Exception as e:
    print(f"ERROR: Failed to initialize embeddings: {e}")
    print("Make sure OPENAI_API_KEY is set in .env")
    exit(1)

# -----------------------------------------------------------------------
# 3. Build FAISS index
# -----------------------------------------------------------------------
print(f"\n[3/3] Building FAISS index from {len(chunks)} chunks...")
print("(This will take a few minutes - embedding in batches)")

try:
    start_time = time.time()
    
    # Build index with FAISS
    vector_store = FAISS.from_documents(
        documents=chunks,
        embedding=embeddings,
        distance_strategy="COSINE"
    )
    
    elapsed = time.time() - start_time
    print(f"✅ Index built in {elapsed:.1f}s")
    
    # Save to disk
    print(f"\nSaving FAISS index to {FAISS_INDEX_PATH}/")
    vector_store.save_local(FAISS_INDEX_PATH)
    print("✅ Index saved")
    
except Exception as e:
    print(f"ERROR: Failed to build index: {e}")
    exit(1)

# -----------------------------------------------------------------------
# Summary
# -----------------------------------------------------------------------
print("\n" + "=" * 70)
print("✅ VECTOR STORE BUILT SUCCESSFULLY")
print("=" * 70)
print(f"Chunks indexed       : {len(chunks):,}")
print(f"Embedding model      : {EMBEDDING_MODEL}")
print(f"Index saved to       : {FAISS_INDEX_PATH}")
print(f"Ready for retrieval  : Yes")
print("\nNext: Run Chatbot.py to ask questions!")
print("=" * 70)
