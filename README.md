A chatbot that answers questions about LLMs and AI using a knowledge base of research papers, docs, and textbooks. Built with LangChain, Pinecone, and OpenAI.

![Python](https://img.shields.io/badge/Python-3.13-blue)
![LangChain](https://img.shields.io/badge/LangChain-1.2.15-green)
![Pinecone](https://img.shields.io/badge/Pinecone-cloud-purple)

---

## What's This?

You ask questions about AI/ML stuff, and it searches through a knowledge base of 6,694 document chunks to find relevant info and give you an answer. It shows you which documents it pulled from, so you can dig deeper if needed.

**What you can ask:**
- "What is LoRA?"
- "How do embeddings work?"
- "Explain attention mechanisms"
- "What's the difference between LoRA and adapters?"

**What it does:**
- Searches 6,694 chunks from 106 documents
- Returns answers grounded in the knowledge base
- Shows source citations so you know where it got info
- Remembers previous questions in a conversation

---

## Knowledge Base

The chatbot knows about:
- 15 arXiv research papers
- 28 Hugging Face docs  
- 21 LangChain docs
- 42 ML/DL textbooks

That's 106 files total, broken into 6,694 chunks for searching.

**Topics covered:** Transformers, LoRA, embeddings, RAG, fine-tuning, attention, etc.

---

## Quick Start

### What You Need
- Python 3.13+
- An OpenAI API key
- A Pinecone API key (free at [pinecone.io](https://pinecone.io))
- Mac/Linux (or Windows with WSL)

### Setup

1. **Clone & enter the directory**
   ```bash
   git clone https://github.com/vidhipitroda/AI-tutor.git
   cd AI-tutor
   ```

2. **Create a virtual environment**
   ```bash
   python3 -m venv .venv
   source .venv/bin/activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Add your API keys to `.env`**
   ```bash
   OPENAI_API_KEY=your-openai-key
   PINECONE_API_KEY=your-pinecone-key
   ```

### Run It

**Web UI (recommended):**
```bash
streamlit run Code/ui_pro.py
```
Open `http://localhost:8502` and you'll see a nice interface with bookmarking features.

**Quick test (CLI):**
```bash
python Code/Chatbot.py "What is LoRA?"
```

**Interactive mode (keep asking questions):**
```bash
python Code/Chatbot.py
# Type questions and hit enter, or type 'exit' to quit
```

---

## Project Structure

```
AI tutor/
├── Code/
│   ├── Chatbot.py              # CLI interface
│   ├── ui_pro.py               # Web UI with bookmarking
│   ├── rag_with_memory.py      # Conversation memory logic
│   ├── upload_to_pinecone.py   # One-time script to upload chunks to Pinecone
│   ├── Ingestion.py            # Load & chunk documents
│   └── verify_cache.py         # Check the cache
│
├── Data/
│   ├── chunks_cache.pkl        # 6,694 chunks (local cache)
│   ├── Papers/                 # 15 PDF papers
│   ├── HF_Docs/                # 28 Hugging Face markdown files
│   ├── LangChain_OpenAI_Docs/  # 21 LangChain docs
│   └── ML_DL_Docs/             # 42 ML/DL guides
│
├── requirements.txt            # Python packages
├── .env                        # Your API keys (don't commit)
└── README.md                   # This file
```

---

## How It Works (The TL;DR)

1. You ask a question
2. It embeds your question into a vector using OpenAI
3. Searches Pinecone (cloud vector DB) for the 5 most similar chunks
4. Sends those chunks + your question to GPT-4o-mini
5. GPT returns an answer with source citations

The whole thing takes 3-5 seconds, mostly OpenAI API latency.

---

## Technical Details

**Libraries used:**
- LangChain 1.2.15 (LLM orchestration)
- Pinecone (cloud vector database — 6,694 chunks stored permanently)
- OpenAI embeddings (convert text to vectors)
- Streamlit (web UI)

**How documents get indexed (one-time setup):**
1. Load all 106 documents
2. Split them into 6,694 chunks (512 tokens each, 64 token overlap)
3. Convert each chunk to a vector using OpenAI embeddings
4. Upload to Pinecone — lives in the cloud permanently
5. App connects to Pinecone on every query, no local files needed

---

## Common Issues

**"ModuleNotFoundError"**
```bash
source .venv/bin/activate
pip install -r requirements.txt
```

**"PINECONE_API_KEY not found"**
```bash
# Add to your .env file
PINECONE_API_KEY=your-key-here
```

**"OpenAI API key error"**
```bash
# Add to your .env file
OPENAI_API_KEY=your-key-here
```

**"Streamlit won't start"**
```bash
pkill -f streamlit
streamlit run Code/ui_pro.py
```

## Deploying to Streamlit Cloud

1. Push your code to GitHub
2. Go to [share.streamlit.io](https://share.streamlit.io)
3. Connect your repo, set main file to `Code/ui_pro.py`
4. Go to **Settings → Secrets** and add:
   ```toml
   OPENAI_API_KEY = "your-key"
   PINECONE_API_KEY = "your-key"
   ```
5. Deploy — no large files needed, Pinecone handles the vector DB

---

## Performance Notes

- Queries take ~3-5 seconds (mostly OpenAI API latency)
- Pinecone search is fast (<100ms)
- No cold start — Pinecone is always on in the cloud

---

## Features

**Web UI (ui_pro.py):**
- 💬 Chat interface with conversation history
- ⭐ Star/bookmark responses you want to save
- 🏷️ Add tags to bookmarks
- 📝 Add notes to responses
- 📤 Export bookmarks as JSON or Markdown
- 📊 See session stats (questions, avg time, bookmarks)

**CLI:**
- Ask single questions or have a conversation
- See source citations immediately

---

## What's Next?

Improvements I'm thinking about:
- Better search with query expansion (HyDE pattern)
- Re-ranking results with cross-encoders
- Document upload so you can add your own knowledge
- Analytics to track what questions people ask most
- Cloud deployment so anyone can use it without installing

---


This for learning and personal projects.

---

Built as a learning project to understand how RAG systems work. Demonstrates document processing, semantic embeddings, vector databases, LLM integration, and web UI development.

**Happy learning! 🚀**
