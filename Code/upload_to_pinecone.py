"""
Upload chunks to Pinecone.
Run this once locally — index lives in the cloud permanently after that.

Steps:
1. Add PINECONE_API_KEY to your .env file
2. Run: python Code/upload_to_pinecone.py
"""

import os
import pickle
import time
from pathlib import Path
from dotenv import load_dotenv
from langchain_openai import OpenAIEmbeddings
from langchain_pinecone import PineconeVectorStore
from pinecone import Pinecone, ServerlessSpec

load_dotenv()

BASE_DIR = Path(__file__).resolve().parent.parent
CACHE_FILE = BASE_DIR / "Data" / "chunks_cache.pkl"
INDEX_NAME = "ai-tutor"
EMBEDDING_MODEL = "text-embedding-3-small"

print("=" * 60)
print("Pinecone Uploader")
print("=" * 60)

# Check keys
if not os.getenv("PINECONE_API_KEY"):
    print("❌ PINECONE_API_KEY not found in .env")
    exit(1)
if not os.getenv("OPENAI_API_KEY"):
    print("❌ OPENAI_API_KEY not found in .env")
    exit(1)

# Load chunks
print("\n[1/3] Loading chunks from cache...")
with open(CACHE_FILE, "rb") as f:
    chunks = pickle.load(f)
print(f"✅ {len(chunks)} chunks loaded")

# Create Pinecone index if it doesn't exist
print("\n[2/3] Setting up Pinecone index...")
pc = Pinecone(api_key=os.getenv("PINECONE_API_KEY"))

existing = [i.name for i in pc.list_indexes()]
if INDEX_NAME not in existing:
    print(f"Creating index '{INDEX_NAME}'...")
    pc.create_index(
        name=INDEX_NAME,
        dimension=1536,  # text-embedding-3-small dimensions
        metric="cosine",
        spec=ServerlessSpec(cloud="aws", region="us-east-1")
    )
    # Wait for it to be ready
    while not pc.describe_index(INDEX_NAME).status["ready"]:
        print("  Waiting for index to be ready...")
        time.sleep(2)
    print("✅ Index created")
else:
    print(f"✅ Index '{INDEX_NAME}' already exists")

# Upload chunks
print(f"\n[3/3] Uploading {len(chunks)} chunks to Pinecone...")
print("  This takes ~2-3 minutes (one-time only)...")

embeddings = OpenAIEmbeddings(model=EMBEDDING_MODEL)

# Upload in batches of 100
batch_size = 100
for i in range(0, len(chunks), batch_size):
    batch = chunks[i:i + batch_size]
    PineconeVectorStore.from_documents(
        documents=batch,
        embedding=embeddings,
        index_name=INDEX_NAME
    )
    print(f"  Uploaded {min(i + batch_size, len(chunks))}/{len(chunks)} chunks...")

print("\n✅ Done! All chunks are now in Pinecone.")
print(f"   Index name: {INDEX_NAME}")
print("   You can now deploy to Streamlit Cloud.")
