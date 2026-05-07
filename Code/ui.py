"""
AI Tutor Chatbot - Streamlit Web UI
Modern, interactive web interface for the RAG chatbot.
"""

import os
import sys
from dotenv import load_dotenv
import streamlit as st
from langchain_openai import ChatOpenAI, OpenAIEmbeddings
from langchain_community.vectorstores import FAISS
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser

# Load environment
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
    page_title="AI Tutor",
    page_icon="🤖",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS
st.markdown("""
<style>
    /* Main styling */
    .main {
        padding-top: 2rem;
    }
    
    /* Chat message styling */
    .chat-message {
        padding: 1rem;
        border-radius: 0.5rem;
        margin-bottom: 1rem;
        display: flex;
        gap: 1rem;
    }
    
    .user-message {
        background-color: #e3f2fd;
        border-left: 4px solid #2196f3;
    }
    
    .assistant-message {
        background-color: #f3e5f5;
        border-left: 4px solid #9c27b0;
    }
    
    .sources-box {
        background-color: #fafafa;
        border: 1px solid #e0e0e0;
        padding: 1rem;
        border-radius: 0.5rem;
        margin-top: 0.5rem;
    }
    
    .source-item {
        padding: 0.5rem;
        margin: 0.25rem 0;
        background-color: #fff;
        border-radius: 0.25rem;
        font-size: 0.9rem;
        border-left: 3px solid #ff9800;
    }
    
    /* Sidebar styling */
    .sidebar-info {
        background-color: #f5f5f5;
        padding: 1rem;
        border-radius: 0.5rem;
        margin-top: 1rem;
    }
</style>
""", unsafe_allow_html=True)

# -----------------------------------------------------------------------
# INITIALIZE SESSION STATE
# -----------------------------------------------------------------------
if "messages" not in st.session_state:
    st.session_state.messages = []

if "vector_store" not in st.session_state:
    st.session_state.vector_store = None

if "llm" not in st.session_state:
    st.session_state.llm = None

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

# -----------------------------------------------------------------------
# RETRIEVE AND ANSWER
# -----------------------------------------------------------------------
def get_answer(question: str, vector_store, llm):
    """Retrieve docs and generate answer"""
    try:
        # Retrieve relevant documents
        retriever = vector_store.as_retriever(search_kwargs={"k": RETRIEVAL_COUNT})
        docs = retriever.invoke(question)
        
        # Format context
        context_str = "\n\n---\n\n".join([
            f"[{doc.metadata.get('source', 'unknown').split('/')[-1]}]\n{doc.page_content}"
            for doc in docs
        ])
        
        # System prompt
        system_prompt = """You are an expert AI tutor helping someone learn about LLMs, machine learning, 
and AI engineering. You have access to high-quality documentation, research papers, and textbooks.

When answering questions:
1. Use ONLY the provided context/documents to answer
2. If the answer isn't in the context, say "I don't have information about this in my knowledge base"
3. Cite which documents/sources you're drawing from
4. Be clear and educational - explain concepts simply
5. For complex topics, break down the answer step-by-step

Context from knowledge base:
{context}"""
        
        prompt_template = ChatPromptTemplate.from_template(system_prompt)
        full_prompt = prompt_template.format(context=context_str)
        
        # Get answer from LLM
        response = llm.invoke(full_prompt + f"\nHuman: {question}\nAssistant:")
        answer = response.content
        
        # Extract sources
        sources = set()
        for doc in docs:
            source = doc.metadata.get("source", "unknown")
            if "/" in source:
                source = source.split("/")[-1]
            sources.add(source)
        
        return answer, sorted(list(sources)), docs
    
    except Exception as e:
        return f"Error: {str(e)}", [], []

# -----------------------------------------------------------------------
# MAIN UI
# -----------------------------------------------------------------------

# Header
col1, col2 = st.columns([1, 4])
with col1:
    st.markdown("# 🤖 AI Tutor")
with col2:
    st.markdown("""
    **Learn LLM & AI Engineering Concepts**  
    Ask questions about transformers, fine-tuning, embeddings, RAG, and more!
    """)

# Initialize on first load
if st.session_state.vector_store is None:
    with st.spinner("Loading vector store..."):
        st.session_state.vector_store = load_vector_store()

if st.session_state.llm is None:
    with st.spinner("Initializing LLM..."):
        st.session_state.llm = load_llm()

if st.session_state.vector_store is None:
    st.error("❌ Failed to load the chatbot. Please check the vector store.")
    st.stop()

# -----------------------------------------------------------------------
# SIDEBAR
# -----------------------------------------------------------------------
with st.sidebar:
    st.header("ℹ️ About")
    st.markdown("""
    ### AI Tutor Chatbot
    
    This chatbot is powered by:
    - **Retrieval-Augmented Generation (RAG)** for accurate answers
    - **FAISS** for semantic search over 6,694+ knowledge chunks
    - **OpenAI GPT-4o-mini** for intelligent responses
    - **Curated Knowledge Base** from research papers & documentation
    
    ### Knowledge Sources
    - 📄 15 Research Papers (arXiv)
    - 📚 28 Hugging Face Documentation
    - 🔗 21 LangChain Docs
    - 📖 42 ML/DL Textbooks
    
    **Total:** 6,694 knowledge chunks indexed
    """)
    
    st.divider()
    
    st.header("💡 Example Questions")
    examples = [
        "What is a transformer?",
        "Explain LoRA fine-tuning",
        "How do embeddings work?",
        "What is RAG?",
        "Explain attention mechanism",
        "What is a tokenizer?"
    ]
    
    if st.button("🔄 Clear Chat History"):
        st.session_state.messages = []
        st.rerun()
    
    st.markdown("Try asking:")
    for example in examples:
        if st.button(example, use_container_width=True):
            st.session_state.input_question = example
            st.rerun()

# -----------------------------------------------------------------------
# CHAT HISTORY
# -----------------------------------------------------------------------
st.divider()

# Display existing messages
for message in st.session_state.messages:
    if message["role"] == "user":
        with st.chat_message("user", avatar="👤"):
            st.markdown(message["content"])
    else:
        with st.chat_message("assistant", avatar="🤖"):
            st.markdown(message["content"])
            if "sources" in message and message["sources"]:
                with st.expander("📚 Sources", expanded=False):
                    for i, source in enumerate(message["sources"], 1):
                        st.markdown(f"**{i}. {source}**")

# -----------------------------------------------------------------------
# INPUT
# -----------------------------------------------------------------------
st.divider()

# Input from sidebar button or chat input
if "input_question" in st.session_state and st.session_state.input_question:
    user_input = st.session_state.input_question
    st.session_state.input_question = None
else:
    user_input = st.chat_input("Ask me anything about LLMs, ML, or AI engineering...")

if user_input:
    # Add user message
    st.session_state.messages.append({
        "role": "user",
        "content": user_input
    })
    
    # Display user message
    with st.chat_message("user", avatar="👤"):
        st.markdown(user_input)
    
    # Get and display assistant response
    with st.chat_message("assistant", avatar="🤖"):
        with st.spinner("Thinking..."):
            answer, sources, docs = get_answer(
                user_input,
                st.session_state.vector_store,
                st.session_state.llm
            )
        
        st.markdown(answer)
        
        # Show sources
        if sources:
            with st.expander("📚 Sources", expanded=False):
                for i, source in enumerate(sources, 1):
                    st.markdown(f"**{i}. {source}**")
    
    # Add assistant message to history
    st.session_state.messages.append({
        "role": "assistant",
        "content": answer,
        "sources": sources
    })

# -----------------------------------------------------------------------
# FOOTER
# -----------------------------------------------------------------------
st.divider()
st.markdown("""
<div style='text-align: center; color: #999; font-size: 0.9rem;'>
    Built with 💜 using LangChain, FAISS, and OpenAI  
    <br>
    For learning LLM & AI Engineering concepts
</div>
""", unsafe_allow_html=True)
