"""
AI Tutor Chatbot - Retrieval-Augmented Generation (RAG)
Answers questions by retrieving relevant chunks from FAISS index
and synthesizing answers with OpenAI GPT-4.
"""
import os
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI, OpenAIEmbeddings
from langchain_community.vectorstores import FAISS
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser

# Load .env
load_dotenv()

# -----------------------------------------------------------------------
# CONFIG
# -----------------------------------------------------------------------
BASE_DIR = "/Users/vidhipitroda/Desktop/Projects/AI tutor"
FAISS_INDEX_PATH = os.path.join(BASE_DIR, "Data/faiss_index")
LLM_MODEL = "gpt-4o-mini"  # Fast & affordable
RETRIEVAL_COUNT = 5  # Top-5 chunks per question

print("=" * 70)
print("AI TUTOR CHATBOT")
print("=" * 70)

# -----------------------------------------------------------------------
# 1. Load FAISS Index
# -----------------------------------------------------------------------
print("\n[Loading vector store...]")
if not os.path.exists(FAISS_INDEX_PATH):
    print(f"ERROR: FAISS index not found at {FAISS_INDEX_PATH}")
    print("Run VectorStore.py first to build the index.")
    exit(1)

try:
    embeddings = OpenAIEmbeddings(model="text-embedding-3-small")
    vector_store = FAISS.load_local(
        FAISS_INDEX_PATH,
        embeddings,
        allow_dangerous_deserialization=True
    )
    print(f"✅ Vector store loaded ({vector_store.index.ntotal} vectors)")
except Exception as e:
    print(f"ERROR: Failed to load vector store: {e}")
    exit(1)

# -----------------------------------------------------------------------
# 2. Initialize LLM
# -----------------------------------------------------------------------
print(f"[Initializing LLM: {LLM_MODEL}...]")
llm = ChatOpenAI(model=LLM_MODEL, temperature=0.7)
print(f"✅ LLM initialized")

# -----------------------------------------------------------------------
# 3. Create RAG System
# -----------------------------------------------------------------------
print("[Setting up RAG system...]")

# System prompt for the chatbot
system_prompt = """You are an expert AI tutor helping someone learn about LLMs, machine learning, 
and AI engineering. You have access to high-quality documentation, research papers, and textbooks.

When answering questions:
1. Use ONLY the provided context/documents to answer
2. If the answer isn't in the context, say "I don't have information about this in my knowledge base"
3. Cite which documents/sources you're drawing from
4. Be clear and educational - explain concepts simply
5. For complex topics, break down the answer step-by-step
6. Give highlevel explanation first, then details breakdown

Context from knowledge base:
{context}"""

print("✅ RAG system ready")
print("=" * 70)

# -----------------------------------------------------------------------
# 4. RAG Function (Manual Implementation)
# -----------------------------------------------------------------------
def answer_question(question: str):
    """Retrieve docs and generate answer"""
    # Retrieve relevant documents
    retriever = vector_store.as_retriever(search_kwargs={"k": RETRIEVAL_COUNT})
    docs = retriever.invoke(question)
    
    # Format context
    context_str = "\n\n---\n\n".join([
        f"[{doc.metadata.get('source', 'unknown').split('/')[-1]}]\n{doc.page_content}"
        for doc in docs
    ])
    
    # Create prompt with context
    full_prompt = system_prompt.format(context=context_str) + f"\n\nHuman: {question}\nAssistant:"
    
    # Get answer from LLM
    response = llm.invoke(full_prompt)
    answer = response.content
    
    return answer, docs

# -----------------------------------------------------------------------
# 5. Interactive Chat Loop
# -----------------------------------------------------------------------
def chat():
    """Interactive chatbot loop"""
    print("\n🤖 AI TUTOR is ready! Ask me anything about LLMs, ML, or AI engineering.")
    print("(Type 'exit' or 'quit' to stop)\n")
    
    while True:
        try:
            question = input("You: ").strip()
            
            if not question:
                continue
            
            if question.lower() in ['exit', 'quit', 'bye', 'done']:
                print("\nTutor: Goodbye! Keep learning! 👋")
                break
            
            print("\nTutor: ", end="", flush=True)
            
            # Get answer
            answer, docs = answer_question(question)
            print(answer)
            
            # Show sources
            if docs:
                print("\n📚 Sources:")
                sources = set()
                for doc in docs:
                    source = doc.metadata.get("source", "unknown")
                    if "/" in source:
                        source = source.split("/")[-1]  # Get just filename
                    sources.add(source)
                
                for i, src in enumerate(sorted(sources), 1):
                    print(f"   {i}. {src}")
            
            print()
        
        except KeyboardInterrupt:
            print("\n\nTutor: Goodbye! 👋")
            break
        except Exception as e:
            print(f"Error: {e}")
            print("Please try again.\n")

# -----------------------------------------------------------------------
# 6. One-shot Query Mode (if question passed as argument)
# -----------------------------------------------------------------------
def query_once(question: str):
    """Answer a single question and exit"""
    print(f"\nYou: {question}")
    print("Tutor: ", end="", flush=True)
    
    answer, docs = answer_question(question)
    print(answer)
    
    if docs:
        print("\n📚 Sources:")
        sources = set()
        for doc in docs:
            source = doc.metadata.get("source", "unknown")
            if "/" in source:
                source = source.split("/")[-1]
            sources.add(source)
        
        for i, src in enumerate(sorted(sources), 1):
            print(f"   {i}. {src}")

# -----------------------------------------------------------------------
# Main
# -----------------------------------------------------------------------
if __name__ == "__main__":
    import sys
    
    if len(sys.argv) > 1:
        # One-shot query mode
        question = " ".join(sys.argv[1:])
        query_once(question)
    else:
        # Interactive mode
        chat()
