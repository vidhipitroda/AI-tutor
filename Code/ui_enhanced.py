"""
Enhanced Streamlit UI with Conversation Memory
Implements Level 2 improvements:
- Multi-turn conversation with context
- Response streaming
- Better formatting
- Analytics
"""

import os
import time
from dotenv import load_dotenv
import streamlit as st
from langchain_openai import ChatOpenAI, OpenAIEmbeddings
from langchain_community.vectorstores import FAISS

# Import our enhanced RAG
import sys
sys.path.insert(0, '/Users/vidhipitroda/Desktop/Projects/AI tutor/Code')
from rag_with_memory import ConversationalRAG, StreamingRAG

load_dotenv()

# -----------------------------------------------------------------------
# CONFIG
# -----------------------------------------------------------------------
BASE_DIR = "/Users/vidhipitroda/Desktop/Projects/AI tutor"
FAISS_INDEX_PATH = os.path.join(BASE_DIR, "Data/faiss_index")
LLM_MODEL = "gpt-4o-mini"
RETRIEVAL_COUNT = 5

# -----------------------------------------------------------------------
# PAGE CONFIG
# -----------------------------------------------------------------------
st.set_page_config(
    page_title="AI Tutor - Enhanced",
    page_icon="🤖",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS
st.markdown("""
<style>
    /* Modern styling */
    .main {
        padding-top: 2rem;
    }
    
    .stChatMessage {
        background-color: #f0f2f6;
        border-radius: 0.5rem;
        padding: 1rem;
        margin: 0.5rem 0;
    }
    
    .conversation-item {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        padding: 1rem;
        border-radius: 0.5rem;
        margin: 0.5rem 0;
    }
    
    .metric-box {
        background: #f0f2f6;
        padding: 1rem;
        border-radius: 0.5rem;
        text-align: center;
        margin: 0.5rem;
    }
</style>
""", unsafe_allow_html=True)

# -----------------------------------------------------------------------
# INITIALIZE SESSION STATE
# -----------------------------------------------------------------------
if "rag_system" not in st.session_state:
    st.session_state.rag_system = None

if "messages" not in st.session_state:
    st.session_state.messages = []

if "conversation_started" not in st.session_state:
    st.session_state.conversation_started = False

if "total_questions" not in st.session_state:
    st.session_state.total_questions = 0

if "total_time" not in st.session_state:
    st.session_state.total_time = 0

# -----------------------------------------------------------------------
# LOAD COMPONENTS
# -----------------------------------------------------------------------
@st.cache_resource
def load_vector_store():
    """Load FAISS index once and cache it"""
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
    """Load LLM once and cache it"""
    return ChatOpenAI(model=LLM_MODEL, temperature=0.7)

@st.cache_resource
def load_streaming_rag(_vector_store, _llm):
    """Create streaming RAG system"""
    return StreamingRAG(_vector_store, _llm)

# -----------------------------------------------------------------------
# MAIN UI
# -----------------------------------------------------------------------

# Header
col1, col2, col3 = st.columns([1, 3, 1])
with col1:
    st.markdown("# 🤖")
with col2:
    st.markdown("# AI Tutor - Smart Learning with Memory")
with col3:
    st.markdown("### v2.0 ⭐")

st.markdown("""
**Learn LLM & AI Engineering with multi-turn conversations**  
I remember what we discussed and provide better answers!
""")

# Initialize components
vector_store = load_vector_store()
llm = load_llm()

if vector_store is None:
    st.error("Failed to load the chatbot. Please check the vector store.")
    st.stop()

# Create RAG system if not exists
if st.session_state.rag_system is None:
    st.session_state.rag_system = load_streaming_rag(vector_store, llm)

rag = st.session_state.rag_system

# -----------------------------------------------------------------------
# SIDEBAR
# -----------------------------------------------------------------------
with st.sidebar:
    st.header("ℹ️ About")
    st.markdown("""
    ### AI Tutor v2.0 - Smart RAG
    
    **What's New:**
    - 💬 **Conversation Memory** - I remember previous questions
    - ⚡ **Streaming Responses** - See answers word-by-word
    - 📖 **Better Context** - Links between related topics
    - 📊 **Analytics** - Track your learning
    
    **Knowledge Base:**
    - 📄 15 Research Papers
    - 📚 28 Hugging Face Docs
    - 🔗 21 LangChain Docs
    - 📖 42 ML/DL Resources
    - **Total:** 6,694 chunks indexed
    """)
    
    st.divider()
    
    # Conversation controls
    st.header("🎮 Controls")
    
    col1, col2 = st.columns(2)
    with col1:
        if st.button("🔄 Clear History", use_container_width=True):
            rag.clear_history()
            st.session_state.messages = []
            st.session_state.total_questions = 0
            st.session_state.total_time = 0
            st.success("History cleared!")
            st.rerun()
    
    with col2:
        if st.button("📊 Show Stats", use_container_width=True):
            st.session_state.show_stats = True
            st.rerun()
    
    st.divider()
    
    # Quick example questions
    st.header("💡 Example Questions")
    examples = [
        "What is a transformer?",
        "Explain LoRA fine-tuning",
        "How do embeddings work?",
        "What is RAG?",
        "How do attention mechanisms work?",
        "When should I use adapters vs LoRA?"
    ]
    
    st.markdown("**Try these follow-up questions:**")
    for example in examples:
        if st.button(example, use_container_width=True, key=f"btn_{example}"):
            st.session_state.input_question = example
            st.rerun()
    
    st.divider()
    
    # Analytics
    if st.session_state.total_questions > 0:
        st.header("📈 Session Stats")
        
        col1, col2 = st.columns(2)
        with col1:
            st.metric("Questions Asked", st.session_state.total_questions)
        with col2:
            avg_time = st.session_state.total_time / st.session_state.total_questions
            st.metric("Avg Response Time", f"{avg_time:.1f}s")

# -----------------------------------------------------------------------
# MAIN CONTENT
# -----------------------------------------------------------------------

# Show conversation history
history = rag.get_history()

if history:
    st.markdown("## 📜 Conversation History")
    
    # Show summary
    summary_col1, summary_col2 = st.columns(2)
    with summary_col1:
        st.metric("Questions in this chat", len(history))
    with summary_col2:
        topics = ", ".join([" ".join(h["question"].split()[:3]) for h in history])
        st.text(f"Topics: {topics}...")
    
    st.divider()

# Display existing messages
for message in st.session_state.messages:
    with st.chat_message(message["role"], avatar="👤" if message["role"] == "user" else "🤖"):
        st.markdown(message["content"])
        
        # Show sources for assistant messages
        if message["role"] == "assistant" and "sources" in message:
            with st.expander("📚 Sources", expanded=False):
                for i, source in enumerate(message["sources"], 1):
                    st.markdown(f"**{i}. {source}**")

# -----------------------------------------------------------------------
# INPUT & RESPONSE
# -----------------------------------------------------------------------

# Get user input
if "input_question" in st.session_state:
    user_input = st.session_state.input_question
    st.session_state.input_question = None
else:
    user_input = st.chat_input("Ask me anything about LLMs, ML, or AI engineering...")

if user_input:
    # Add user message to display
    with st.chat_message("user", avatar="👤"):
        st.markdown(user_input)
    
    st.session_state.messages.append({
        "role": "user",
        "content": user_input
    })
    
    # Generate response with streaming
    with st.chat_message("assistant", avatar="🤖"):
        response_placeholder = st.empty()
        sources_placeholder = st.empty()
        
        # Measure response time
        start_time = time.time()
        
        # Stream response
        full_response = ""
        try:
            for token in rag.stream_answer(user_input):
                full_response += token
                # Update display with streaming text
                response_placeholder.markdown(full_response + "▌")  # Cursor animation
            
            # Remove cursor and show final response
            response_placeholder.markdown(full_response)
            
            # Get docs for sources
            docs = rag.retriever.invoke(user_input)
            sources = [doc.metadata.get("source", "unknown").split("/")[-1] for doc in docs]
            
            # Show sources
            with sources_placeholder.container():
                with st.expander("📚 Sources", expanded=False):
                    for i, source in enumerate(sources, 1):
                        st.markdown(f"**{i}. {source}**")
            
        except Exception as e:
            response_placeholder.error(f"Error: {str(e)}")
            full_response = f"Error: {str(e)}"
        
        # Record response time
        response_time = time.time() - start_time
        st.session_state.total_questions += 1
        st.session_state.total_time += response_time
        
        # Add to messages
        st.session_state.messages.append({
            "role": "assistant",
            "content": full_response,
            "sources": sources if 'sources' in locals() else [],
            "response_time": response_time
        })
    
    # Show response time
    st.caption(f"⏱️ Response time: {response_time:.2f}s")
    
    # Show conversation memory indicator
    if len(history) > 1:
        st.info(f"💭 Using memory from {len(history)-1} previous question(s)")

# -----------------------------------------------------------------------
# FOOTER
# -----------------------------------------------------------------------
st.divider()

col1, col2, col3 = st.columns(3)
with col1:
    st.caption("Built with LangChain + FAISS + OpenAI")
with col2:
    st.caption("Version 2.0 - Conversational RAG")
with col3:
    st.caption("🚀 Learning RAG in action")
