import os
import pickle
from collections import Counter

CACHE_FILE = "/Users/vidhipitroda/Desktop/Projects/AI tutor/Data/chunks_cache.pkl"

# -----------------------------------------------------------------------
# 1. Check cache exists
# -----------------------------------------------------------------------
if not os.path.exists(CACHE_FILE):
    print("ERROR: Cache file not found!")
    print(f"Expected at: {CACHE_FILE}")
    print("Run Ingestion.py first to build the cache.")
    exit(1)

size_mb = os.path.getsize(CACHE_FILE) / (1024 * 1024)
print(f"Cache file found: {CACHE_FILE}")
print(f"File size: {size_mb:.2f} MB\n")

# -----------------------------------------------------------------------
# 2. Load cache
# -----------------------------------------------------------------------
print("Loading cache...")
with open(CACHE_FILE, "rb") as f:
    chunks = pickle.load(f)

print(f"Total chunks loaded: {len(chunks)}\n")

# -----------------------------------------------------------------------
# 3. Break down by source
# -----------------------------------------------------------------------
source_counts = Counter()
for chunk in chunks:
    source = chunk.metadata.get("source", "unknown")
    # Categorize by folder name
    if "/Papers/" in source:
        label = "Papers (PDFs)"
    elif "/HF_Docs/" in source:
        label = "HF_Docs"
    elif "/LangChain_OpenAI_Docs/" in source:
        label = "LangChain_OpenAI_Docs"
    elif "/ML_DL_Docs/" in source:
        label = "ML_DL_Docs"
    else:
        label = f"Other ({source})"
    source_counts[label] += 1

print("--- Chunks by source ---")
for label, count in sorted(source_counts.items()):
    print(f"  {label:<30} {count:>6} chunks")

# -----------------------------------------------------------------------
# 4. Spot-check: print 3 random samples
# -----------------------------------------------------------------------
import random
print("\n--- Sample chunks (random) ---")
samples = random.sample(chunks, min(3, len(chunks)))
for i, chunk in enumerate(samples):
    source = chunk.metadata.get("source", "unknown")
    print(f"\n[Sample {i+1}]")
    print(f"  Source : {source}")
    print(f"  Length : {len(chunk.page_content)} chars")
    print(f"  Preview: {chunk.page_content[:200].strip()!r}")

# -----------------------------------------------------------------------
# 5. Basic health checks
# -----------------------------------------------------------------------
print("\n--- Health checks ---")
empty_chunks = [c for c in chunks if not c.page_content.strip()]
print(f"  Empty chunks    : {len(empty_chunks)}")

avg_len = sum(len(c.page_content) for c in chunks) / len(chunks)
print(f"  Avg chunk length: {avg_len:.0f} chars")

min_len = min(len(c.page_content) for c in chunks)
max_len = max(len(c.page_content) for c in chunks)
print(f"  Min chunk length: {min_len} chars")
print(f"  Max chunk length: {max_len} chars")

print("\nVerification complete!")
