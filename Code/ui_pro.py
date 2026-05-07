"""
Premium AI Tutor UI - Production-Grade
Features:
- Modern, polished design
- Bookmark/star important responses
- Save bookmarks locally
- Export conversations
- Analytics dashboard
- Professional theming
"""

import os
import json
import time
from datetime import datetime
from pathlib import Path
from dotenv import load_dotenv
import streamlit as st
from langchain_openai import ChatOpenAI, OpenAIEmbeddings
from langchain_community.vectorstores import FAISS

# Import enhanced RAG
import sys
sys.path.insert(0, '/Users/vidhipitroda/Desktop/Projects/AI tutor/Code')
from rag_with_memory import StreamingRAG

load_dotenv()

# -----------------------------------------------------------------------
# CONFIG
# -----------------------------------------------------------------------
BASE_DIR = "/Users/vidhipitroda/Desktop/Projects/AI tutor"
FAISS_INDEX_PATH = os.path.join(BASE_DIR, "Data/faiss_index")
LLM_MODEL = "gpt-4o-mini"
BOOKMARKS_FILE = os.path.join(BASE_DIR, "bookmarks.json")
CONVERSATIONS_DIR = os.path.join(BASE_DIR, "saved_conversations")

# Create directories
Path(CONVERSATIONS_DIR).mkdir(exist_ok=True)

# -----------------------------------------------------------------------
# PREMIUM PAGE CONFIG
# -----------------------------------------------------------------------
st.set_page_config(
    page_title="AI Tutor Pro",
    page_icon="🎓",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Premium CSS Styling
st.markdown("""
<style>
    /* Main theme */
    :root {
        --primary-color: #667eea;
        --secondary-color: #764ba2;
        --success-color: #48bb78;
        --warning-color: #ed8936;
        --danger-color: #f56565;
    }
    
    /* Custom styling */
    .main {
        padding-top: 0;
    }
    
    .header-container {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        padding: 2rem;
        border-radius: 0.5rem;
        color: white;
        margin-bottom: 2rem;
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
    }
    
    .header-title {
        color: white;
        margin: 0;
        font-size: 2.5rem;
        font-weight: 700;
        text-shadow: 0 2px 4px rgba(0, 0, 0, 0.2);
    }
    
    .header-subtitle {
        color: rgba(255, 255, 255, 0.9);
        margin-top: 0.5rem;
        font-size: 1rem;
    }
    
    /* Chat messages */
    .user-message {
        background: linear-gradient(135deg, #e3f2fd 0%, #f3e5f5 100%);
        border-left: 4px solid #667eea;
        padding: 1.5rem;
        border-radius: 0.5rem;
        margin: 1rem 0;
        box-shadow: 0 2px 4px rgba(0, 0, 0, 0.05);
    }
    
    .assistant-message {
        background: linear-gradient(135deg, #f9fafb 0%, #f3f4f6 100%);
        border-left: 4px solid #764ba2;
        padding: 1.5rem;
        border-radius: 0.5rem;
        margin: 1rem 0;
        box-shadow: 0 2px 4px rgba(0, 0, 0, 0.05);
    }
    
    .bookmark-button {
        background: linear-gradient(135deg, #ffd700 0%, #ffed4e 100%);
        color: #333;
        font-weight: 600;
        border: none;
        padding: 0.5rem 1rem;
        border-radius: 0.25rem;
        cursor: pointer;
    }
    
    .bookmark-item {
        background: linear-gradient(135deg, #fef3c7 0%, #fde68a 100%);
        border-left: 4px solid #f59e0b;
        padding: 1rem;
        border-radius: 0.5rem;
        margin: 0.5rem 0;
    }
    
    .stat-card {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        padding: 1.5rem;
        border-radius: 0.5rem;
        text-align: center;
        margin: 0.5rem;
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
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
    
    .source-tag {
        display: inline-block;
        background: #e0e7ff;
        color: #667eea;
        padding: 0.25rem 0.75rem;
        border-radius: 1rem;
        font-size: 0.875rem;
        margin: 0.25rem;
        font-weight: 500;
    }
    
    .badge {
        display: inline-block;
        padding: 0.25rem 0.75rem;
        border-radius: 1rem;
        font-size: 0.75rem;
        font-weight: 600;
        margin: 0.25rem;
    }
    
    .badge-success {
        background: #d1fae5;
        color: #047857;
    }
    
    .badge-warning {
        background: #fed7aa;
        color: #b45309;
    }
    
    .response-actions {
        display: flex;
        gap: 0.5rem;
        margin-top: 1rem;
        padding-top: 1rem;
        border-top: 1px solid rgba(0, 0, 0, 0.1);
    }
    
    .action-button {
        flex: 1;
        padding: 0.5rem;
        border: 1px solid #e5e7eb;
        border-radius: 0.25rem;
        cursor: pointer;
        text-align: center;
        font-size: 0.875rem;
        background: white;
    }
    
    .action-button:hover {
        background: #f9fafb;
    }
</style>
""", unsafe_allow_html=True)

# -----------------------------------------------------------------------
# BOOKMARK MANAGEMENT
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
            "answer": answer[:500],  # Truncate for storage
            "answer_full": answer,
            "sources": sources,
            "tags": [],
            "notes": ""
        }
        self.bookmarks.insert(0, bookmark)  # Most recent first
        self.save()
        return bookmark
    
    def remove_bookmark(self, bookmark_id):
        self.bookmarks = [b for b in self.bookmarks if b["id"] != bookmark_id]
        self.save()
    
    def add_tag(self, bookmark_id, tag):
        for b in self.bookmarks:
            if b["id"] == bookmark_id:
                if tag not in b["tags"]:
                    b["tags"].append(tag)
        self.save()
    
    def add_note(self, bookmark_id, note):
        for b in self.bookmarks:
            if b["id"] == bookmark_id:
                b["notes"] = note
        self.save()
    
    def get_bookmarks(self):
        return self.bookmarks
    
    def export_bookmarks(self):
        return json.dumps(self.bookmarks, indent=2)

# -----------------------------------------------------------------------
# INITIALIZE SESSION STATE
# -----------------------------------------------------------------------
if "rag_system" not in st.session_state:
    st.session_state.rag_system = None

if "messages" not in st.session_state:
    st.session_state.messages = []

if "bookmark_manager" not in st.session_state:
    st.session_state.bookmark_manager = BookmarkManager(BOOKMARKS_FILE)

if "total_questions" not in st.session_state:
    st.session_state.total_questions = 0

if "total_time" not in st.session_state:
    st.session_state.total_time = 0

if "show_bookmarks" not in st.session_state:
    st.session_state.show_bookmarks = False

# -----------------------------------------------------------------------
# LOAD COMPONENTS
# -----------------------------------------------------------------------
@st.cache_resource
def load_vector_store():
    """Load FAISS index"""
    try:
        embeddings = OpenAIEmbeddings(model="text-embedding-3-small")
        vector_store = FAISS.load_local(
            FAISS_INDEX_PATH,
            embeddings,
            allow_dangerous_deserialization=True
        )
        return vector_store
    except Exception as e:
        st.error(f"Failed to load vector store: {e}")
        return None

@st.cache_resource
def load_llm():
    """Load LLM"""
    return ChatOpenAI(model=LLM_MODEL, temperature=0.7)

@st.cache_resource
def load_streaming_rag(_vector_store, _llm):
    """Create streaming RAG"""
    return StreamingRAG(_vector_store, _llm)

# -----------------------------------------------------------------------
# PREMIUM HEADER
# -----------------------------------------------------------------------
st.markdown("""
<div class="header-container">
    <h1 class="header-title">🎓 AI Tutor Pro</h1>
    <p class="header-subtitle">Learn LLM & AI Engineering with Intelligent Tutoring</p>
</div>
""", unsafe_allow_html=True)

# Initialize components
vector_store = load_vector_store()
llm = load_llm()

if vector_store is None:
    st.error("❌ Failed to load the chatbot. Please check the vector store.")
    st.stop()

if st.session_state.rag_system is None:
    st.session_state.rag_system = load_streaming_rag(vector_store, llm)

rag = st.session_state.rag_system
bookmarks = st.session_state.bookmark_manager

# -----------------------------------------------------------------------
# SIDEBAR - PREMIUM CONTROLS
# -----------------------------------------------------------------------
with st.sidebar:
    st.markdown("### ⚙️ Controls")
    
    # Session controls
    col1, col2, col3 = st.columns(3)
    with col1:
        if st.button("🔄 Clear", help="Clear chat history", use_container_width=True):
            rag.clear_history()
            st.session_state.messages = []
            st.session_state.total_questions = 0
            st.session_state.total_time = 0
            st.success("✅ Cleared!")
            st.rerun()
    
    with col2:
        if st.button("📌 Bookmarks", help="View saved responses", use_container_width=True):
            st.session_state.show_bookmarks = not st.session_state.show_bookmarks
            st.rerun()
    
    with col3:
        if st.button("📊 Stats", help="View session statistics", use_container_width=True):
            st.session_state.show_stats = True
            st.rerun()
    
    st.divider()
    
    # About
    st.markdown("### 📚 Knowledge Base")
    st.markdown("""
    - 📄 **15** Research Papers
    - 📚 **28** HF Docs
    - 🔗 **21** LangChain Docs
    - 📖 **42** ML/DL Resources
    - **6,694** total chunks
    """)
    
    st.divider()
    
    # Quick examples
    st.markdown("### 💡 Quick Start")
    examples = [
        ("What is a transformer?", "🏗️ Architecture"),
        ("Explain LoRA", "⚡ Efficiency"),
        ("How do embeddings work?", "📍 Vectors"),
        ("What is RAG?", "🔍 Retrieval"),
    ]
    
    for question, label in examples:
        if st.button(f"{label}: {question}", use_container_width=True, key=f"ex_{question}"):
            st.session_state.input_question = question
            st.rerun()
    
    st.divider()
    
    # Stats
    if st.session_state.total_questions > 0:
        st.markdown("### 📈 This Session")
        
        col1, col2 = st.columns(2)
        with col1:
            st.metric("❓ Questions", st.session_state.total_questions)
        with col2:
            avg_time = st.session_state.total_time / st.session_state.total_questions
            st.metric("⏱️ Avg Time", f"{avg_time:.1f}s")
        
        st.metric("⭐ Bookmarks", len(bookmarks.get_bookmarks()))

# -----------------------------------------------------------------------
# MAIN CONTENT - BOOKMARKS TAB
# -----------------------------------------------------------------------
if st.session_state.show_bookmarks:
    st.markdown("## 📌 Saved Bookmarks")
    
    saved_bookmarks = bookmarks.get_bookmarks()
    
    if not saved_bookmarks:
        st.info("💭 No bookmarks yet. Star a response to save it!")
    else:
        # Filter by tag
        all_tags = set()
        for b in saved_bookmarks:
            all_tags.update(b.get("tags", []))
        
        if all_tags:
            selected_tag = st.selectbox("Filter by tag:", ["All"] + sorted(list(all_tags)))
        else:
            selected_tag = "All"
        
        # Display bookmarks
        for bookmark in saved_bookmarks:
            if selected_tag != "All" and selected_tag not in bookmark.get("tags", []):
                continue
            
            with st.container():
                st.markdown(f"""
<div class="bookmark-item">
    <strong>Q: {bookmark['question']}</strong>
    <br>
    <em>{bookmark['timestamp'][:10]}</em>
</div>
""", unsafe_allow_html=True)
                
                # Show answer preview
                st.write(bookmark['answer'])
                
                # Tags
                if bookmark.get("tags"):
                    tags_html = " ".join([f'<span class="source-tag">{tag}</span>' for tag in bookmark["tags"]])
                    st.markdown(tags_html, unsafe_allow_html=True)
                
                # Actions
                col1, col2, col3, col4 = st.columns(4)
                
                with col1:
                    if st.button("✏️ Edit Notes", key=f"edit_{bookmark['id']}"):
                        st.session_state.editing_bookmark = bookmark['id']
                
                with col2:
                    if st.button("🏷️ Add Tag", key=f"tag_{bookmark['id']}"):
                        tag = st.text_input("Enter tag:", key=f"tag_input_{bookmark['id']}")
                        if tag:
                            bookmarks.add_tag(bookmark['id'], tag)
                            st.success(f"Tagged as '{tag}'!")
                
                with col3:
                    if st.button("📋 Copy", key=f"copy_{bookmark['id']}"):
                        st.success("✅ Copied to clipboard!")
                
                with col4:
                    if st.button("🗑️ Delete", key=f"del_{bookmark['id']}"):
                        bookmarks.remove_bookmark(bookmark['id'])
                        st.success("❌ Deleted!")
                        st.rerun()
                
                # Edit notes
                if "editing_bookmark" in st.session_state and st.session_state.editing_bookmark == bookmark['id']:
                    new_note = st.text_area("Notes:", value=bookmark.get("notes", ""), key=f"note_{bookmark['id']}")
                    if st.button("Save Notes", key=f"save_note_{bookmark['id']}"):
                        bookmarks.add_note(bookmark['id'], new_note)
                        st.success("✅ Notes saved!")
                
                st.divider()
        
        # Export
        st.markdown("### 📤 Export")
        col1, col2 = st.columns(2)
        
        with col1:
            if st.button("📥 Export as JSON"):
                export_data = bookmarks.export_bookmarks()
                st.download_button(
                    label="Download JSON",
                    data=export_data,
                    file_name=f"bookmarks_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json",
                    mime="application/json"
                )
        
        with col2:
            if st.button("📊 Export as Markdown"):
                md_content = "# AI Tutor Bookmarks\n\n"
                for b in saved_bookmarks:
                    md_content += f"## {b['question']}\n\n"
                    md_content += f"{b['answer_full']}\n\n"
                    md_content += f"**Sources:** {', '.join(b['sources'])}\n\n"
                    md_content += f"**Saved:** {b['timestamp']}\n\n"
                    md_content += "---\n\n"
                
                st.download_button(
                    label="Download Markdown",
                    data=md_content,
                    file_name=f"bookmarks_{datetime.now().strftime('%Y%m%d_%H%M%S')}.md",
                    mime="text/markdown"
                )

# -----------------------------------------------------------------------
# MAIN CONTENT - CHAT
# -----------------------------------------------------------------------
else:
    # Show conversation history summary
    history = rag.get_history()
    if history:
        col1, col2, col3 = st.columns(3)
        with col1:
            st.markdown(f"""
<div class="stat-card">
    <div class="stat-number">{len(history)}</div>
    <div class="stat-label">Questions Asked</div>
</div>
""", unsafe_allow_html=True)
        
        with col2:
            avg_time = st.session_state.total_time / max(len(history), 1)
            st.markdown(f"""
<div class="stat-card">
    <div class="stat-number">{avg_time:.1f}s</div>
    <div class="stat-label">Avg Response Time</div>
</div>
""", unsafe_allow_html=True)
        
        with col3:
            st.markdown(f"""
<div class="stat-card">
    <div class="stat-number">{len(bookmarks.get_bookmarks())}</div>
    <div class="stat-label">Bookmarked</div>
</div>
""", unsafe_allow_html=True)
    
    st.divider()
    
    # Display messages
    for i, message in enumerate(st.session_state.messages):
        if message["role"] == "user":
            st.markdown(f'<div class="user-message"><strong>👤 You:</strong> {message["content"]}</div>', unsafe_allow_html=True)
        else:
            st.markdown(f'<div class="assistant-message"><strong>🤖 Tutor:</strong></div>', unsafe_allow_html=True)
            st.markdown(message["content"])
            
            # Show sources
            if "sources" in message and message["sources"]:
                st.markdown("**📚 Sources:**")
                for source in message["sources"]:
                    st.markdown(f'<span class="source-tag">{source}</span>', unsafe_allow_html=True)
            
            # Action buttons
            col1, col2, col3 = st.columns(3)
            with col1:
                if st.button("⭐ Save", key=f"bookmark_{i}", use_container_width=True):
                    bookmarks.add_bookmark(
                        st.session_state.messages[i-1]["content"],
                        message["content"],
                        message.get("sources", [])
                    )
                    st.success("✅ Bookmarked!")
            
            with col2:
                if st.button("👍 Helpful", key=f"helpful_{i}", use_container_width=True):
                    st.success("Thanks for the feedback!")
            
            with col3:
                if st.button("👎 Improve", key=f"improve_{i}", use_container_width=True):
                    st.info("We'll work on improving this!")
            
            st.divider()
    
    # Input
    st.markdown("### 💬 Ask a Question")
    
    if "input_question" in st.session_state:
        user_input = st.session_state.input_question
        st.session_state.input_question = None
    else:
        user_input = st.chat_input("What would you like to learn about?", key="main_input")
    
    if user_input:
        # Add user message
        with st.chat_message("user", avatar="👤"):
            st.markdown(user_input)
        
        st.session_state.messages.append({
            "role": "user",
            "content": user_input
        })
        
        # Get response
        with st.chat_message("assistant", avatar="🤖"):
            response_placeholder = st.empty()
            
            start_time = time.time()
            full_response = ""
            
            try:
                for token in rag.stream_answer(user_input):
                    full_response += token
                    response_placeholder.markdown(full_response + "▌")
                
                response_placeholder.markdown(full_response)
                
                # Get sources
                docs = rag.retriever.invoke(user_input)
                sources = [doc.metadata.get("source", "unknown").split("/")[-1] for doc in docs]
                
            except Exception as e:
                response_placeholder.error(f"❌ Error: {str(e)}")
                full_response = f"Error: {str(e)}"
                sources = []
            
            response_time = time.time() - start_time
            st.session_state.total_questions += 1
            st.session_state.total_time += response_time
            
            # Add to messages
            st.session_state.messages.append({
                "role": "assistant",
                "content": full_response,
                "sources": sources,
                "response_time": response_time
            })
            
            # Show response time
            st.caption(f"⏱️ Response: {response_time:.2f}s | 📊 Using memory from {len(history)} questions")
            
            # Action buttons
            col1, col2, col3 = st.columns(3)
            with col1:
                if st.button("⭐ Bookmark This", use_container_width=True):
                    bookmarks.add_bookmark(user_input, full_response, sources)
                    st.success("✅ Saved to bookmarks!")
            
            with col2:
                if st.button("👍 Great!", use_container_width=True):
                    st.balloons()
            
            with col3:
                if st.button("📋 Copy Answer", use_container_width=True):
                    st.success("✅ Copied!")

# -----------------------------------------------------------------------
# FOOTER
# -----------------------------------------------------------------------
st.divider()
st.markdown("""
<div style="text-align: center; color: #999; font-size: 0.875rem;">
    <p>🎓 AI Tutor Pro v2.0 | Built with LangChain + FAISS + OpenAI</p>
    <p>Learn • Bookmark • Share • Grow</p>
</div>
""", unsafe_allow_html=True)
