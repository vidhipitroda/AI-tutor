"""
AI Tutor - Modern Professional UI
Clean, minimalist design with smooth interactions
"""

import os
import json
import time
import html
from datetime import datetime
from pathlib import Path
from dotenv import load_dotenv
import streamlit as st
from langchain_openai import OpenAIEmbeddings
from langchain_groq import ChatGroq
from langchain_pinecone import PineconeVectorStore

# Import enhanced RAG
import sys
BASE_DIR = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(BASE_DIR / "Code"))
from rag_with_memory import StreamingRAG

load_dotenv()

# -----------------------------------------------------------------------
# CONFIG
# -----------------------------------------------------------------------
BOOKMARKS_FILE = str(BASE_DIR / "bookmarks.json")
CONVERSATIONS_DIR = str(BASE_DIR / "saved_conversations")
Path(CONVERSATIONS_DIR).mkdir(exist_ok=True)

# -----------------------------------------------------------------------
# PAGE CONFIG
# -----------------------------------------------------------------------
st.set_page_config(
    page_title="AI Tutor",
    page_icon="🤖",
    layout="wide",
    initial_sidebar_state="expanded"
)

# -----------------------------------------------------------------------
# MODERN CSS
# -----------------------------------------------------------------------
st.markdown("""
<style>
    /* Import modern font */
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap');
    
    /* Global styles */
    * {
        font-family: 'Inter', -apple-system, BlinkMacSystemFont, sans-serif;
    }
    
    /* Hide Streamlit branding */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
    
    /* Hide empty containers */
    div[data-testid="stVerticalBlock"]:empty {
        display: none;
    }
    
    div[data-testid="stHorizontalBlock"]:empty {
        display: none;
    }
    
    /* Main container */
    .main {
        background: linear-gradient(135deg, #f5f7fa 0%, #c3cfe2 100%);
        padding: 0 !important;
        max-width: 100%;
    }
    
    .block-container {
        padding: 2rem 3rem !important;
        max-width: 1200px;
        margin: 0 auto;
    }
    
    /* Header */
    .header {
        background: white;
        padding: 2rem 3rem;
        border-radius: 20px;
        box-shadow: 0 8px 32px rgba(0, 0, 0, 0.08);
        margin-bottom: 2rem;
        border: 1px solid rgba(255, 255, 255, 0.8);
        backdrop-filter: blur(10px);
    }
    
    .header h1 {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        font-size: 2.5rem;
        font-weight: 700;
        margin: 0;
        letter-spacing: -0.02em;
    }
    
    .header p {
        color: #64748b;
        font-size: 1rem;
        margin: 0.5rem 0 0 0;
        font-weight: 400;
    }
    
    /* Chat container */
    .chat-container {
        background: white;
        border-radius: 20px;
        box-shadow: 0 8px 32px rgba(0, 0, 0, 0.08);
        padding: 2rem;
        margin-bottom: 2rem;
        border: 1px solid rgba(255, 255, 255, 0.8);
    }
    
    /* Message bubbles */
    .message {
        padding: 1.25rem 1.5rem;
        border-radius: 16px;
        margin: 1rem 0;
        animation: slideIn 0.3s ease-out;
    }
    
    @keyframes slideIn {
        from {
            opacity: 0;
            transform: translateY(10px);
        }
        to {
            opacity: 1;
            transform: translateY(0);
        }
    }
    
    .user-message {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        margin-left: 20%;
        box-shadow: 0 4px 16px rgba(102, 126, 234, 0.3);
    }
    
    .assistant-message {
        background: #f8fafc;
        border: 1px solid #e2e8f0;
        margin-right: 20%;
        color: #1e293b;
    }
    
    .message strong {
        display: block;
        margin-bottom: 0.5rem;
        font-weight: 600;
        font-size: 0.875rem;
        opacity: 0.9;
    }
    
    /* Source tags */
    .source-tag {
        display: inline-block;
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        padding: 0.375rem 0.875rem;
        border-radius: 20px;
        font-size: 0.75rem;
        margin: 0.25rem 0.25rem 0.25rem 0;
        font-weight: 500;
        box-shadow: 0 2px 8px rgba(102, 126, 234, 0.25);
    }
    
    /* Buttons */
    .stButton > button {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        border: none;
        border-radius: 12px;
        padding: 0.75rem 1.5rem;
        font-weight: 600;
        font-size: 0.9375rem;
        transition: all 0.3s ease;
        box-shadow: 0 4px 16px rgba(102, 126, 234, 0.3);
        width: 100%;
    }
    
    .stButton > button:hover {
        transform: translateY(-2px);
        box-shadow: 0 6px 20px rgba(102, 126, 234, 0.4);
    }
    
    /* Input */
    .stTextInput > div > div > input {
        border-radius: 12px;
        border: 2px solid #e2e8f0;
        padding: 0.875rem 1rem;
        font-size: 0.9375rem;
        transition: all 0.2s ease;
    }
    
    .stTextInput > div > div > input:focus {
        border-color: #667eea;
        box-shadow: 0 0 0 3px rgba(102, 126, 234, 0.1);
    }
    
    /* Sidebar */
    [data-testid="stSidebar"] {
        background: white;
        border-right: 1px solid #e2e8f0;
    }
    
    /* Hide sidebar collapse button */
    [data-testid="collapsedControl"] {
        display: none !important;
    }
    
    button[kind="header"] {
        display: none !important;
    }
    
    /* Force sidebar buttons to be equal width */
    [data-testid="stSidebar"] [data-testid="column"] {
        width: 50% !important;
        flex: 1 1 50% !important;
    }
    
    [data-testid="stSidebar"] .stButton > button {
        background: white;
        color: #667eea;
        border: 2px solid #667eea;
        box-shadow: none;
    }
    
    [data-testid="stSidebar"] .stButton > button:hover {
        background: #667eea;
        color: white;
    }
    
    /* Stats cards */
    .stat-card {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        padding: 1.5rem;
        border-radius: 16px;
        text-align: center;
        box-shadow: 0 4px 16px rgba(102, 126, 234, 0.3);
    }
    
    .stat-number {
        font-size: 2rem;
        font-weight: 700;
        margin: 0;
    }
    
    .stat-label {
        font-size: 0.875rem;
        opacity: 0.9;
        margin-top: 0.5rem;
    }
    
    /* Action buttons row */
    .action-row {
        display: flex;
        gap: 0.5rem;
        margin-top: 1rem;
    }
    
    .action-btn {
        flex: 1;
        padding: 0.625rem;
        background: white;
        border: 2px solid #e2e8f0;
        border-radius: 10px;
        text-align: center;
        cursor: pointer;
        transition: all 0.2s ease;
        font-size: 0.875rem;
        font-weight: 500;
    }
    
    .action-btn:hover {
        border-color: #667eea;
        color: #667eea;
        transform: translateY(-1px);
    }
    
    /* Loading animation */
    .loading {
        display: inline-block;
        width: 8px;
        height: 8px;
        border-radius: 50%;
        background: #667eea;
        animation: pulse 1.5s ease-in-out infinite;
    }
    
    @keyframes pulse {
        0%, 100% { opacity: 1; }
        50% { opacity: 0.3; }
    }
    
    /* Scrollbar */
    ::-webkit-scrollbar {
        width: 8px;
        height: 8px;
    }
    
    ::-webkit-scrollbar-track {
        background: #f1f5f9;
        border-radius: 4px;
    }
    
    ::-webkit-scrollbar-thumb {
        background: #cbd5e1;
        border-radius: 4px;
    }
    
    ::-webkit-scrollbar-thumb:hover {
        background: #94a3b8;
    }
    
    /* Responsive */
    @media (max-width: 768px) {
        .block-container {
            padding: 1rem !important;
        }
        
        .header h1 {
            font-size: 2rem;
        }
        
        .user-message, .assistant-message {
            margin-left: 0 !important;
            margin-right: 0 !important;
        }
    }
</style>
""", unsafe_allow_html=True)

# -----------------------------------------------------------------------
# BOOKMARK MANAGER
# -----------------------------------------------------------------------
class BookmarkManager:
    def __init__(self, file_path):
        self.file_path = file_path
        self.load()
    
    def load(self):
        if os.path.exists(self.file_path):
            with open(self.file_path) as f:
                self.bookmarks = json.load(f)
        else:
            self.bookmarks = []
    
    def save(self):
        with open(self.file_path, 'w') as f:
            json.dump(self.bookmarks, f, indent=2)
    
    def add_bookmark(self, question, answer, sources):
        bookmark = {
            "id": len(self.bookmarks) + 1,
            "timestamp": datetime.now().isoformat(),
            "question": question,
            "answer": answer[:500],
            "answer_full": answer,
            "sources": sources,
            "tags": [],
            "notes": ""
        }
        self.bookmarks.insert(0, bookmark)
        self.save()
        return bookmark
    
    def remove_bookmark(self, bookmark_id):
        self.bookmarks = [b for b in self.bookmarks if b["id"] != bookmark_id]
        self.save()
    
    def get_bookmarks(self):
        self.load()  # Reload from file to get latest
        return self.bookmarks

# -----------------------------------------------------------------------
# SESSION STATE
# -----------------------------------------------------------------------
if 'messages' not in st.session_state:
    st.session_state.messages = []
if 'rag_system' not in st.session_state:
    st.session_state.rag_system = None
if 'bookmark_manager' not in st.session_state:
    st.session_state.bookmark_manager = BookmarkManager(BOOKMARKS_FILE)
if 'total_questions' not in st.session_state:
    st.session_state.total_questions = 0
if 'total_time' not in st.session_state:
    st.session_state.total_time = 0
if 'show_bookmarks' not in st.session_state:
    st.session_state.show_bookmarks = False

# -----------------------------------------------------------------------
# LOAD COMPONENTS
# -----------------------------------------------------------------------
@st.cache_resource
def load_vector_store():
    """Load vector store from Pinecone"""
    try:
        pinecone_key = os.getenv("PINECONE_API_KEY") or st.secrets.get("PINECONE_API_KEY", "")
        openai_key = os.getenv("OPENAI_API_KEY") or st.secrets.get("OPENAI_API_KEY", "")

        if not pinecone_key or not openai_key:
            st.error("❌ API keys not found. Add them to secrets.")
            return None

        os.environ["PINECONE_API_KEY"] = pinecone_key
        os.environ["OPENAI_API_KEY"] = openai_key

        embeddings = OpenAIEmbeddings(model="text-embedding-3-small")
        vector_store = PineconeVectorStore(
            index_name="ai-tutor",
            embedding=embeddings
        )
        return vector_store
    except Exception as e:
        st.error(f"Failed to load vector store: {e}")
        return None

@st.cache_resource
def load_llm():
    """Load Groq LLM"""
    groq_key = os.getenv("GROQ_API_KEY") or st.secrets.get("GROQ_API_KEY", "")
    if not groq_key:
        st.error("❌ GROQ_API_KEY not found")
        return None
    os.environ["GROQ_API_KEY"] = groq_key
    return ChatGroq(model="llama-3.3-70b-versatile", temperature=0.7)

@st.cache_resource
def load_streaming_rag(_vector_store, _llm):
    """Create streaming RAG"""
    return StreamingRAG(_vector_store, _llm)

# -----------------------------------------------------------------------
# HEADER
# -----------------------------------------------------------------------
st.markdown("""
<div class="header">
    <h1>🤖 AI Tutor</h1>
    <p>Your intelligent assistant for AI & Machine Learning concepts</p>
</div>
""", unsafe_allow_html=True)

# Initialize components
vector_store = load_vector_store()
llm = load_llm()

if vector_store is None or llm is None:
    st.error("❌ Failed to initialize. Please check your API keys.")
    st.stop()

if st.session_state.rag_system is None:
    st.session_state.rag_system = load_streaming_rag(vector_store, llm)

rag = st.session_state.rag_system
bookmarks = st.session_state.bookmark_manager

# -----------------------------------------------------------------------
# SIDEBAR
# -----------------------------------------------------------------------
with st.sidebar:
    st.title("🎯 AI Tutor Menu")
    st.markdown("### ⚙️ Controls")
    
    col1, col2 = st.columns(2)
    with col1:
        if st.button("🗑️ Clear Chat", use_container_width=True):
            st.session_state.messages = []
            rag.clear_history()
            st.rerun()
    
    with col2:
        if st.button("📌 Bookmarks", use_container_width=True):
            st.session_state.show_bookmarks = not st.session_state.show_bookmarks
            st.rerun()
    
    st.divider()
    
    st.markdown("### 📊 Stats")
    st.metric("Bookmarks", len(bookmarks.get_bookmarks()))
    if st.session_state.total_questions > 0:
        avg_time = st.session_state.total_time / st.session_state.total_questions
        st.metric("Questions", st.session_state.total_questions)
        st.metric("Avg Time", f"{avg_time:.1f}s")
    
    st.divider()
    
    st.markdown("### 💡 Try asking")
    examples = [
        "What is LoRA?",
        "Explain attention mechanisms",
        "How do embeddings work?",
        "What's RAG?"
    ]
    
    for q in examples:
        if st.button(q, key=f"ex_{q}", use_container_width=True):
            st.session_state.input_question = q
            st.rerun()
    
    st.divider()
    
    st.markdown("### 📚 Knowledge Base")
    st.markdown("""
    - 15 Research Papers
    - 28 HuggingFace Docs
    - 21 LangChain Docs
    - 42 ML/DL Resources
    
    **6,694 chunks indexed**
    """)

# -----------------------------------------------------------------------
# BOOKMARKS VIEW
# -----------------------------------------------------------------------
if st.session_state.show_bookmarks:
    col1, col2 = st.columns([4, 1])
    with col1:
        st.markdown("## 📌 Saved Bookmarks")
    with col2:
        if st.button("← Back to Chat", use_container_width=True):
            st.session_state.show_bookmarks = False
            st.rerun()
    
    st.divider()
    
    saved_bookmarks = bookmarks.get_bookmarks()
    
    if not saved_bookmarks:
        st.info("💭 No bookmarks yet. Star a response to save it!")
    else:
        for bookmark in saved_bookmarks:
            with st.container():
                question = html.escape(bookmark['question']).replace('\n', '<br>')
                answer = html.escape(bookmark['answer_full']).replace('\n', '<br>')
                st.markdown(f"""
                <div class="message assistant-message">
                    <strong>Q: {question}</strong>
                    <p>{answer}</p>
                    <small style="opacity: 0.7;">Saved on {bookmark['timestamp'][:10]}</small>
                </div>
                """, unsafe_allow_html=True)
                
                if bookmark.get("sources"):
                    sources_html = " ".join([f'<span class="source-tag">{s}</span>' for s in bookmark["sources"]])
                    st.markdown(sources_html, unsafe_allow_html=True)
                
                col1, col2 = st.columns([3, 1])
                with col2:
                    if st.button("🗑️ Delete", key=f"del_{bookmark['id']}"):
                        bookmarks.remove_bookmark(bookmark['id'])
                        st.rerun()
                
                st.divider()

# -----------------------------------------------------------------------
# CHAT VIEW
# -----------------------------------------------------------------------
else:
    # Welcome message when no chat
    if not st.session_state.messages:
        st.markdown("""
        <div style="text-align: center; padding: 4rem 2rem; color: #64748b;">
            <h2 style="font-weight: 600; margin-bottom: 1rem;">👋 Ask me anything about AI & ML</h2>
            <p>I can help you understand concepts from research papers, documentation, and textbooks.</p>
        </div>
        """, unsafe_allow_html=True)
    else:
        # Display messages in container
        st.markdown('<div class="chat-container">', unsafe_allow_html=True)
        
        for i, message in enumerate(st.session_state.messages):
            if message["role"] == "user":
                content = html.escape(message["content"]).replace('\n', '<br>')
                st.markdown(f"""
                <div class="message user-message">
                    <strong>You</strong>
                    <p>{content}</p>
                </div>
                """, unsafe_allow_html=True)
            else:
                content = html.escape(message["content"]).replace('\n', '<br>')
                st.markdown(f"""
                <div class="message assistant-message">
                    <strong>AI Tutor</strong>
                    <p>{content}</p>
                </div>
                """, unsafe_allow_html=True)
                
                if "sources" in message and message["sources"]:
                    sources_html = " ".join([f'<span class="source-tag">{s}</span>' for s in message["sources"]])
                    st.markdown(sources_html, unsafe_allow_html=True)
                
                # Action buttons
                col1, col2, col3 = st.columns(3)
                with col1:
                    if st.button("⭐ Save", key=f"save_{i}", use_container_width=True):
                        user_q = st.session_state.messages[i-1]["content"] if i > 0 else "Unknown"
                        bookmarks.add_bookmark(user_q, message["content"], message.get("sources", []))
                        st.success("✅ Bookmarked!")
                        time.sleep(1)
                        st.rerun()
                with col2:
                    if st.button("👍 Helpful", key=f"up_{i}", use_container_width=True):
                        st.success("Thanks!")
                with col3:
                    if st.button("📋 Copy", key=f"copy_{i}", use_container_width=True):
                        st.success("Copied!")
        
        st.markdown('</div>', unsafe_allow_html=True)
    
    # Input
    user_input = st.chat_input("Ask a question about AI, ML, or deep learning...")
    
    if "input_question" in st.session_state and st.session_state.input_question:
        user_input = st.session_state.input_question
        st.session_state.input_question = None
    
    if user_input:
        # Add user message
        st.session_state.messages.append({
            "role": "user",
            "content": user_input
        })
        
        # Get response
        start_time = time.time()
        full_response = ""
        
        with st.spinner("🤔 Thinking..."):
            try:
                for token in rag.stream_answer(user_input):
                    full_response += token
                
                docs = rag.retriever.invoke(user_input)
                sources = [doc.metadata.get("source", "unknown").split("/")[-1] for doc in docs]
                
            except Exception as e:
                full_response = f"❌ Error: {str(e)}"
                sources = []
        
        response_time = time.time() - start_time
        st.session_state.total_questions += 1
        st.session_state.total_time += response_time
        
        st.session_state.messages.append({
            "role": "assistant",
            "content": full_response,
            "sources": sources,
            "response_time": response_time
        })
        
        st.rerun()

# -----------------------------------------------------------------------
# FOOTER
# -----------------------------------------------------------------------
st.markdown("""
<div style="text-align: center; padding: 2rem; color: #94a3b8; font-size: 0.875rem;">
    <p>Built with LangChain, Pinecone, Groq & OpenAI</p>
</div>
""", unsafe_allow_html=True)
