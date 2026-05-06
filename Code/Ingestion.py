import os
import pickle
import glob
import fitz  # pymupdf — much faster than PyPDFLoader
os.environ.setdefault("USER_AGENT", "AITutor/1.0")

from langchain_community.document_loaders import TextLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_core.documents import Document

# -----------------------------------------------------------------------
# PATHS
# -----------------------------------------------------------------------
BASE       = "/Users/vidhipitroda/Desktop/Projects/AI tutor/Data"
CACHE_FILE = os.path.join(BASE, "chunks_cache.pkl")
PAPERS_DIR = os.path.join(BASE, "Papers")
HF_DIR     = os.path.join(BASE, "HF_Docs")
LC_DIR     = os.path.join(BASE, "LangChain_OpenAI_Docs")

# -----------------------------------------------------------------------
# PATH VERIFICATION
# -----------------------------------------------------------------------
print("=== Path Check ===")
for name, path in [("Base", BASE), ("Papers", PAPERS_DIR), ("HF_Docs", HF_DIR), ("LangChain_Docs", LC_DIR)]:
    exists = os.path.isdir(path)
    count  = len(os.listdir(path)) if exists else 0
    print(f"  {'OK' if exists else 'MISSING'} {name}: {path}  ({count} files)")
print()

splitter = RecursiveCharacterTextSplitter(chunk_size=512, chunk_overlap=64)

# -----------------------------------------------------------------------

def load_pdfs(folder):
    pdf_files = sorted(glob.glob(os.path.join(folder, "*.pdf")))
    print(f"Loading {len(pdf_files)} PDFs from {os.path.basename(folder)}/")
    if not pdf_files:
        print("  WARNING: No PDF files found! Check the folder path above.")
        return []
    all_chunks = []
    for i, path in enumerate(pdf_files):
        name = os.path.basename(path)
        try:
            # pymupdf is 5-10x faster than PyPDFLoader
            doc = fitz.open(path)
            pages = [
                Document(
                    page_content=page.get_text(),
                    metadata={"source": path, "page": page.number}
                )
                for page in doc
                if page.get_text().strip()  # skip blank pages
            ]
            doc.close()
            doc_chunks = splitter.split_documents(pages)
            all_chunks.extend(doc_chunks)
            print(f"  [{i+1}/{len(pdf_files)}] {name} -> {len(pages)} pages, {len(doc_chunks)} chunks")
        except Exception as e:
            print(f"  Skipped {name}: {e}")
    return all_chunks


def load_text_files(folder, label):
    txt_files = sorted(glob.glob(os.path.join(folder, "*.txt")))
    print(f"Loading {len(txt_files)} text files from {label}/")
    if not txt_files:
        print(f"  WARNING: No .txt files found! Check the folder path above.")
        return []
    all_chunks = []
    for i, path in enumerate(txt_files):
        name = os.path.basename(path)
        try:
            docs = TextLoader(path, encoding="utf-8").load()
            doc_chunks = splitter.split_documents(docs)
            all_chunks.extend(doc_chunks)
            print(f"   [{i+1}/{len(txt_files)}] {name} -> {len(doc_chunks)} chunks")
        except Exception as e:
            print(f"   Skipped {name}: {e}")
    return all_chunks


# -----------------------------------------------------------------------
# MAIN
# -----------------------------------------------------------------------
if os.path.exists(CACHE_FILE):
    print("Loading chunks from cache...")
    with open(CACHE_FILE, "rb") as f:
        chunks = pickle.load(f)
    print(f"Ready! {len(chunks)} chunks loaded from cache.")

else:
    print("Cache not found - building knowledge base from all data sources...")
    chunks = []

    chunks += load_pdfs(PAPERS_DIR)
    print(f"   -> Running total: {len(chunks)} chunks")

    chunks += load_text_files(HF_DIR, "HF_Docs")
    print(f"   -> Running total: {len(chunks)} chunks")

    chunks += load_text_files(LC_DIR, "LangChain_OpenAI_Docs")
    print(f"   -> Running total: {len(chunks)} chunks")

    print(f"\nSaving {len(chunks)} chunks to cache...")
    with open(CACHE_FILE, "wb") as f:
        pickle.dump(chunks, f)
    print(f"Done! Cache saved to {CACHE_FILE}")
    print("Next run will load instantly from cache.")

print(f"\nSummary: {len(chunks)} total chunks ready for retrieval.")
