# 🤖 AI Tutor - LLM Learning Chatbot

An intelligent retrieval-augmented generation (RAG) chatbot designed to help you learn LLM and AI engineering concepts. Built with state-of-the-art tools: **LangChain**, **FAISS**, **OpenAI**, and **Streamlit**.

![Python](https://img.shields.io/badge/Python-3.13-blue)
![LangChain](https://img.shields.io/badge/LangChain-1.2.15-green)
![FAISS](https://img.shields.io/badge/FAISS-1.13.2-orange)
![License](https://img.shields.io/badge/License-MIT-purple)

---

## 📚 Project Overview

This project implements a **Retrieval-Augmented Generation (RAG)** system that:

1. **Ingests** curated knowledge from multiple sources (research papers, documentation)
2. **Chunks** documents into manageable segments with overlap
3. **Embeds** chunks using OpenAI embeddings into a vector database
4. **Retrieves** the most relevant chunks based on semantic similarity
5. **Synthesizes** intelligent answers using GPT-4 with retrieved context

### Key Features

✅ **Interactive Web UI** - Built with Streamlit for easy access  
✅ **Semantic Search** - FAISS vector database with 6,694 indexed chunks  
✅ **Multi-Source Knowledge** - 106 files from 4 knowledge sources  
✅ **Source Attribution** - Shows which documents informed each answer  
✅ **Context-Aware** - Only answers based on knowledge base  
✅ **Educational Focus** - Designed for learning LLM & AI concepts

## 🏗️ Architecture

```
User Query
    ↓
Embedding (OpenAI text-embedding-3-small)
    ↓
FAISS Similarity Search (retrieve top-5 chunks)
    ↓
Combine with System Prompt
    ↓
GPT-4o-mini LLM
    ↓
Answer + Source Citations
```

---

## 📊 Knowledge Base

The chatbot has access to **6,694 knowledge chunks** from:

| Source | Files | Type |
|--------|-------|------|
| arXiv Papers | 15 | PDF |
| Hugging Face Docs | 28 | Markdown |
| LangChain Docs | 21 | Markdown |
| ML/DL Textbooks | 42 | Markdown |
| **Total** | **106** | — |

Topics covered:
- Transformers & Attention Mechanisms
- Fine-tuning (LoRA, QLoRA, Adapters)
- Embeddings & Vector Databases
- Retrieval-Augmented Generation (RAG)
- Large Language Models (LLMs)
- Training Techniques & Optimization
- And much more!

---

## 🚀 Quick Start

### Prerequisites

- **Python 3.13+**
- **OpenAI API Key** (for embeddings and LLM)
- **Mac/Linux** (or Windows with WSL2)

### Installation

1. **Clone the repository**
   ```bash
   git clone https://github.com/vidhipitroda/AI-tutor.git
   cd AI-tutor
   ```

2. **Create virtual environment**
   ```bash
   python3 -m venv .venv
   source .venv/bin/activate  # On Windows: .venv\Scripts\activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Set up environment variables**
   ```bash
   cp .env.example .env
   # Edit .env and add your OpenAI API key
   export OPENAI_API_KEY="sk-proj-your-key-here"
   ```

5. **Verify the vector store exists**
   ```bash
   # If Data/faiss_index/ doesn't exist, run:
   python Code/VectorStore.py
   ```

### Using the Chatbot

**Interactive mode:**
```bash
source .venv/bin/activate
python Code/Chatbot.py
```

Then type your questions:
```
You: What is LoRA?
You: Explain attention mechanism
You: How does transformer architecture work?
```

Type `exit` or `quit` to stop.

**Single question mode:**
```bash
python Code/Chatbot.py "What is LoRA?"
```

## 📁 Project Structure

```
AI tutor/
├── Code/
│   ├── Chatbot.py                      # Main interactive RAG chatbot
│   ├── VectorStore.py                  # Build FAISS index (6,694 vectors)
│   ├── Ingestion.py                    # Load docs, create chunks cache
│   ├── verify_cache.py                 # Inspect chunks cache
│   └── download_*.py                   # Download scripts (4 sources)
│
├── Data/
│   ├── chunks_cache.pkl                # 6,694 document chunks (3.1 MB)
│   ├── faiss_index/                    # FAISS vector index
│   │   ├── index.faiss
│   │   └── index.pkl
## 💻 Usage

### Option 1: Web UI (Recommended)

Launch the interactive Streamlit web interface:

```bash
./run_ui.sh
```

Or manually:
```bash
cd /Users/vidhipitroda/Desktop/Projects/AI\ tutor
source .venv/bin/activate
streamlit run Code/ui.py
```

Then open your browser to `http://localhost:8501`

**Features:**
- 💬 Multi-turn conversation history
- 📚 Source document citations
- 💡 Quick example questions
- 🔄 Clear chat history button
- 🎨 Modern, responsive design

### Option 2: Command Line

Ask a single question:

```bash
python Code/Chatbot.py "What is LoRA?"
```

Output:
```
You: What is LoRA?
Tutor: LoRA (Low-Rank Adaptation) is a fine-tuning technique...

📚 Sources:
   1. lora_paper.pdf
   2. fine_tuning_guide.md
```

### Option 3: Interactive Terminal

Start an interactive chat session:

```bash
python Code/Chatbot.py
```

Then ask multiple questions:
```
You: What is a transformer?
Tutor: A transformer is...

📚 Sources:
   1. attention_is_all_you_need.pdf
   
You: How does attention work?
Tutor: Attention is a mechanism...

You: exit
Tutor: Goodbye! Keep learning! 👋
```

---

## 📁 Project Structure

```
AI tutor/
├── Code/
│   ├── Ingestion.py          # Load & chunk documents (6,694 chunks)
│   ├── VectorStore.py        # Build FAISS index from chunks
│   ├── Chatbot.py            # CLI chatbot (manual RAG)
│   ├── ui.py                 # Streamlit web UI
│   └── verify_cache.py       # Cache health check
│
├── Data/
│   ├── chunks_cache.pkl      # Cached document chunks (3.1 MB)
│   ├── faiss_index/          # FAISS vector database
│   │   ├── index.faiss       # Main index file
│   │   └── index.pkl         # Index metadata
│   ├── Papers/               # 15 arXiv PDFs
│   ├── HF_Docs/              # 28 Hugging Face markdown docs
│   ├── LangChain_OpenAI_Docs/# 21 LangChain docs
│   └── ML_DL_Docs/           # 42 ML/DL textbooks
│
├── run_ui.sh                 # Streamlit startup script
├── requirements.txt          # Python dependencies
├── .env                      # Environment variables (git-ignored)
├── .gitignore               # Exclude large files from git
└── README.md                # This file
```

---

## 🔧 Technical Stack

### Core Libraries

| Library | Version | Purpose |
|---------|---------|---------|
| LangChain | 1.2.15 | LLM orchestration & RAG |
| langchain-core | 1.3.2 | Core abstractions |
| langchain-openai | 1.2.1 | OpenAI integration |
| langchain-community | 0.4.1 | Community integrations |
| FAISS | 1.13.2 | Vector similarity search |
| PyMuPDF | Latest | Fast PDF loading |
| Streamlit | 1.57.0 | Web UI framework |
| python-dotenv | 1.2.2 | Environment config |

### External APIs

- **OpenAI API**
  - `text-embedding-3-small` - Fast & cheap embeddings (1,000 dims)
  - `gpt-4o-mini` - Fast & affordable LLM

---

## 🏃 Pipeline Details

### 1. Data Ingestion (`Ingestion.py`)

```python
# Loads PDFs (fast with PyMuPDF) and text files
# Chunks with overlap for better retrieval
# Saves to disk cache for reuse

Inputs:  Data/Papers/, Data/HF_Docs/, etc.
Process: RecursiveCharacterTextSplitter(512/64)
Output:  Data/chunks_cache.pkl (6,694 chunks)
```

### 2. Vector Indexing (`VectorStore.py`)

```python
# Embeds all chunks using OpenAI
# Builds FAISS index for similarity search
# Stores index on disk for fast loading

Inputs:  Data/chunks_cache.pkl
Process: OpenAIEmbeddings(text-embedding-3-small)
         FAISS.from_documents()
Output:  Data/faiss_index/ (ready for retrieval)
```

### 3. Retrieval-Augmented Generation

```python
# Retrieves top-5 most similar chunks
# Formats as context for the LLM prompt
# Generates answer grounded in knowledge base

User Query → Embed → FAISS Retrieval → Format Prompt → GPT-4o-mini → Answer
```

---

## 🎯 Example Questions

The chatbot can help with questions like:

- **Fundamentals**: "What is a transformer?", "How do embeddings work?"
- **Techniques**: "What is LoRA?", "Explain QLoRA fine-tuning"
- **Concepts**: "What is RAG?", "How does attention work?"
- **Applications**: "When should I use vector databases?", "How to build a chatbot?"
- **Implementation**: "What's the difference between adapters and LoRA?"

---

## ⚙️ Configuration

### Environment Variables (`.env`)

```bash
OPENAI_API_KEY=sk-proj-your-key-here
```

### Chatbot Parameters

Edit in `Code/Chatbot.py` or `Code/ui.py`:

```python
LLM_MODEL = "gpt-4o-mini"      # Model to use
RETRIEVAL_COUNT = 5             # Top-K chunks to retrieve
TEMPERATURE = 0.7               # Response creativity (0-1)
```

### Chunk Settings

Edit in `Code/Ingestion.py`:

```python
chunk_size = 512                # Tokens per chunk
chunk_overlap = 64              # Overlap between chunks
```

---

## 🔄 Regenerate Vector Store

If you want to rebuild the knowledge base:

```bash
# Re-ingest and cache all documents
python Code/Ingestion.py

# Rebuild FAISS index
python Code/VectorStore.py

# Verify the cache
python Code/verify_cache.py
```

---

## 🐛 Troubleshooting

### Issue: "ModuleNotFoundError: No module named 'langchain'"

**Solution:**
```bash
source .venv/bin/activate
pip install -r requirements.txt
```

### Issue: "FAISS index not found"

**Solution:**
```bash
python Code/VectorStore.py
```

This regenerates the index from the cached chunks.

### Issue: "OpenAI API key not found"

**Solution:**
```bash
export OPENAI_API_KEY="sk-proj-your-key-here"
# Or add to .env file
```

### Issue: Streamlit won't start

**Solution:**
```bash
# Kill any existing Streamlit processes
pkill -f streamlit

# Try again with debug mode
streamlit run Code/ui.py --logger.level=debug
```

---

## 📈 Performance

- **Embedding Speed**: ~19.8 seconds for 6,694 chunks
- **FAISS Retrieval**: <100ms per query
- **LLM Response**: ~2-5 seconds (via OpenAI API)
- **Total Response Time**: ~3-6 seconds end-to-end

---

## 🤝 Contributing

This is a personal learning project, but feel free to:
- ✅ Fork and customize for your learning
- ✅ Add more knowledge sources
- ✅ Improve the UI
- ✅ Optimize performance

---

## � License

MIT License - Feel free to use this for learning and personal projects.

---

## 🎓 Learning Journey

Built as part of learning LLM engineering. The project demonstrates:

- ✅ Document processing & chunking strategies
- ✅ Semantic embeddings & vector databases
- ✅ Retrieval-augmented generation (RAG)
- ✅ LLM integration & prompt engineering
- ✅ Web UI development with Streamlit
- ✅ End-to-end ML pipeline

---

## 🙏 Acknowledgments

- **LangChain** - For excellent LLM orchestration framework
- **OpenAI** - For powerful embeddings & LLMs
- **FAISS** - For fast similarity search
- **Streamlit** - For simple web app development

---

## 📧 Contact

Created by **Vidhi Pitroda**  
Learning to become an AI Engineer 🚀

---

**Happy Learning! 🎓**

*Last Updated: May 2026*

**Q: "FAISS index not found"**
- Run `python Code/VectorStore.py` first

**Q: "OpenAI API key error"**
- Create `.env` file: `echo "OPENAI_API_KEY=sk-proj-..." > .env`
- Check key at [platform.openai.com](https://platform.openai.com/api-keys)

**Q: "ModuleNotFoundError"**
- Activate venv: `source .venv/bin/activate`
- Reinstall packages: `pip install -r requirements.txt`

## 📝 Future Enhancements

- [ ] Web UI (Streamlit/Gradio)
- [ ] Multi-turn conversation memory
- [ ] Custom document upload
- [ ] Source highlighting
- [ ] Export conversations
- [ ] Faster embedding model options
- [ ] Conversation history persistence

## 👨‍💻 Author

Built as a learning project to master LLM engineering concepts through a practical RAG implementation.

## 📚 References

- [Attention is All You Need](https://arxiv.org/abs/1706.03762)
- [LoRA: Low-Rank Adaptation](https://arxiv.org/abs/2106.09685)
- [RAG: Retrieval-Augmented Generation](https://arxiv.org/abs/2005.11401)
- [LangChain Documentation](https://docs.langchain.com/)
- [Hugging Face Transformers](https://huggingface.co/docs/transformers/)

---

**Last Updated**: 2024
**Status**: ✅ Fully Functional
