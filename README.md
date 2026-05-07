Hello heloo

# 🎓 AI Tutor

A chatbot that answers questions about LLMs and AI using a knowledge base of research papers, docs, and textbooks. Built with LangChain, FAISS, and OpenAI.

![Python](https://img.shields.io/badge/Python-3.13-blue)
![LangChain](https://img.shields.io/badge/LangChain-1.2.15-green)
![FAISS](https://img.shields.io/badge/FAISS-1.13.2-orange)
![License](https://img.shields.io/badge/License-MIT-purple)

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

4. **Add your OpenAI API key**
   ```bash
   cp .env.example .env
   # Edit .env and add your key
   export OPENAI_API_KEY="sk-proj-your-key-here"
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
│   ├── Chatbot.py           # CLI interface
│   ├── ui_pro.py            # Web UI with bookmarking
│   ├── rag_with_memory.py   # Conversation memory logic
│   ├── VectorStore.py       # Build the FAISS index
│   ├── Ingestion.py         # Load & chunk documents
│   └── verify_cache.py      # Check the cache
│
├── Data/
│   ├── chunks_cache.pkl     # 6,694 chunks stored here
│   ├── faiss_index/         # Vector database
│   ├── Papers/              # 15 PDF papers
│   ├── HF_Docs/             # 28 Hugging Face markdown files
│   ├── LangChain_OpenAI_Docs/  # 21 LangChain docs
│   └── ML_DL_Docs/          # 42 ML/DL guides
│
├── requirements.txt         # Python packages
├── .env                     # Your OpenAI key (don't commit)
└── README.md                # This file
```

---

## How It Works (The TL;DR)

1. You ask a question
2. It embeds your question into a vector
3. Searches FAISS for the 5 most similar document chunks
4. Sends those chunks + your question to GPT-4o-mini
5. GPT returns an answer with source citations

The whole thing takes 3-6 seconds. First query is slower because it loads the vector database into memory.

---

## Technical Details

**Libraries used:**
- LangChain 1.2.15 (LLM stuff)
- FAISS 1.13.2 (fast vector search)
- OpenAI embeddings (convert text to vectors)
- Streamlit (web UI)

**How documents get indexed:**
1. Load all 106 documents
2. Split them into 6,694 chunks (512 tokens each, 64 token overlap)
3. Convert each chunk to a vector using OpenAI embeddings
4. Store in FAISS for fast searching
5. Save to disk so we don't have to rebuild every time

---

## Common Issues

**"ModuleNotFoundError"**
```bash
source .venv/bin/activate
pip install -r requirements.txt
```

**"FAISS index not found"**
```bash
python Code/VectorStore.py
```

**"OpenAI API key error"**
```bash
export OPENAI_API_KEY="sk-proj-your-key-here"
# Or create a .env file with your key
```

**"Streamlit won't start"**
```bash
pkill -f streamlit
streamlit run Code/ui_pro.py
```

---

## Performance Notes

- First query: ~5-6 seconds (loads the vector database)
- After that: ~3-4 seconds per query
- FAISS search is fast (<100ms), most time is the OpenAI API

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

## License

MIT - Do whatever you want with this for learning and personal projects.

---

Built as a learning project to understand how RAG systems work. Demonstrates document processing, semantic embeddings, vector databases, LLM integration, and web UI development.

**Happy learning! 🚀**
