# AI Tutor - LLM Learning Chatbot

An intelligent retrieval-augmented generation (RAG) chatbot designed to help you learn about Large Language Models, machine learning, and AI engineering concepts.

## 🎯 Project Overview

This project implements a **Retrieval-Augmented Generation (RAG)** pipeline that combines:
- **Knowledge Base**: 106 curated documents (15 research papers, 28 Hugging Face docs, 21 LangChain docs, 42 ML/DL resources)
- **Vector Embeddings**: OpenAI text-embedding-3-small for semantic search
- **Vector Store**: FAISS for efficient similarity search across 6,694 document chunks
- **LLM**: OpenAI GPT-4o-mini for generating educational responses

The chatbot answers your questions about AI/ML topics by searching the knowledge base and synthesizing answers with proper source citations.

## 🏗️ Architecture

```
┌─────────────────────────────────────────────────────────┐
│                    USER QUESTION                        │
└────────────────────┬────────────────────────────────────┘
                     │
                     ▼
        ┌──────────────────────────┐
        │   Embed Question         │
        │  (OpenAI embeddings)     │
        └──────────────┬───────────┘
                       │
                       ▼
        ┌──────────────────────────┐
        │  Retrieve Top-5 Chunks   │
        │  (FAISS similarity)      │
        └──────────────┬───────────┘
                       │
                       ▼
        ┌──────────────────────────┐
        │  Format Context          │
        │  (chunk + source)        │
        └──────────────┬───────────┘
                       │
                       ▼
        ┌──────────────────────────────────┐
        │  Send to LLM (GPT-4o-mini)       │
        │  with system prompt + context    │
        └──────────────┬────────────────────┘
                       │
                       ▼
        ┌──────────────────────────────────┐
        │  Generate Educational Answer     │
        │  with Source Citations           │
        └──────────────┬────────────────────┘
                       │
                       ▼
┌─────────────────────────────────────────────────────────┐
│                  CHATBOT RESPONSE                       │
└─────────────────────────────────────────────────────────┘
```

## 📊 Data Pipeline

```
Raw Documents (106 files)
    │
    ├── Papers/ (15 arXiv PDFs)
    ├── HF_Docs/ (28 Hugging Face markdown files)
    ├── LangChain_OpenAI_Docs/ (21 LangChain docs)
    └── ML_DL_Docs/ (42 ML/DL resources)
    │
    ▼
Code/Ingestion.py
    ├─ Load PDFs (pymupdf - 5-10x faster)
    ├─ Load TXT files (TextLoader)
    └─ Chunk documents (512 chars, 64 overlap)
    │
    ▼
Data/chunks_cache.pkl (3.1 MB, 6,694 chunks)
    │
    ▼
Code/VectorStore.py
    ├─ Embed chunks (text-embedding-3-small)
    └─ Build FAISS index
    │
    ▼
Data/faiss_index/ (FAISS vector index)
    │
    ▼
Code/Chatbot.py (Interactive RAG chatbot)
```

## 🚀 Quick Start

### Prerequisites
- Python 3.13+
- OpenAI API key (set in `.env` file)

### Installation

1. **Clone/Navigate to project:**
   ```bash
   cd /Users/vidhipitroda/Desktop/Projects/AI\ tutor
   ```

2. **Create and activate virtual environment:**
   ```bash
   python3 -m venv .venv
   source .venv/bin/activate
   ```

3. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

4. **Set up environment variables:**
   ```bash
   # Create .env file with your OpenAI API key
   echo "OPENAI_API_KEY=sk-proj-your-key-here" > .env
   ```

### Building the Knowledge Base (One-time setup)

If you need to rebuild the knowledge base:

```bash
# 1. Download documents (already in Data/)
python Code/download_papers.py
python Code/download_hf_docs.py
python Code/download_langchain_openai_docs.py
python Code/download_ml_dl_docs.py

# 2. Create chunks cache
python Code/Ingestion.py

# 3. Build vector store (6,694 chunks → FAISS index in 19.8s)
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
│   ├── Papers/                         # 15 arXiv PDFs
│   ├── HF_Docs/                        # 28 Hugging Face docs
│   ├── LangChain_OpenAI_Docs/          # 21 LangChain docs
│   ├── ML_DL_Docs/                     # 42 ML/DL resources
│   └── Machine learning sources.txt
│
├── .env                                # OpenAI API key (git-ignored)
├── .gitignore
├── requirements.txt
└── README.md
```

## 🔧 Technologies

### Core Libraries
- **LangChain** (1.2.15): LLM orchestration framework
- **OpenAI**: GPT-4o-mini (LLM) + text-embedding-3-small (embeddings)
- **FAISS**: Vector similarity search (6,694 embeddings)
- **pymupdf (fitz)**: Fast PDF parsing (5-10x faster than PyPDFLoader)

### Embedding & Storage
- **OpenAI text-embedding-3-small**: 384-dimensional embeddings
- **FAISS**: CPU-based vector index (COSINE distance metric)
- **pickle**: Chunk caching for fast reloads

## 📈 Performance Metrics

- **Embedding Speed**: 6,694 chunks embedded in 19.8 seconds
- **Vector Store Size**: ~200 MB (FAISS index)
- **Chunk Cache Size**: 3.1 MB (pickle)
- **Retrieval Speed**: ~100ms per query (top-5 documents)
- **LLM Response**: ~2-5 seconds (GPT-4o-mini)

## 🎓 Knowledge Base Coverage

### Domain Coverage
- **Transformers & Attention**: attention mechanisms, transformer architecture, BERT, GPT models
- **Parameter Efficiency**: LoRA, QLoRA, prefix tuning, adapter modules
- **Fine-tuning Strategies**: supervised fine-tuning, RLHF, instruction tuning
- **Vector Embeddings**: semantic search, embedding models, similarity metrics
- **LLM Development**: prompt engineering, RAG, chatbot architectures
- **Deep Learning Fundamentals**: neural networks, optimization, backpropagation
- **ML Tools**: Hugging Face, LangChain, scikit-learn, PyTorch basics

### Source Quality
- 15 peer-reviewed research papers (arXiv)
- 28 official Hugging Face documentation pages
- 21 LangChain official documentation pages
- 42 ML/DL textbook chapters and tutorials

## 💡 Example Queries

```bash
# Model architecture
"What is the transformer architecture?"
"Explain attention mechanisms"
"How does BERT work?"

# Parameter efficiency
"What is LoRA?"
"Explain QLoRA and when to use it"
"Compare different parameter-efficient tuning methods"

# LLM concepts
"What is prompt engineering?"
"Explain retrieval-augmented generation (RAG)"
"How does fine-tuning differ from in-context learning?"

# Implementation
"How to fine-tune a model with Hugging Face?"
"What are the best practices for building a chatbot?"
"Explain the RAG pipeline"
```

## 🔐 Security & Privacy

- **API Keys**: `.env` file excluded from git (see `.gitignore`)
- **Data**: Knowledge base stored locally (no external API calls for search)
- **Embeddings**: Only OpenAI embeddings require API calls
- **Cache**: Pickle cache stored locally for fast startup

## 🛠️ Development

### Verify Chunk Cache
```bash
python Code/verify_cache.py
```

Output shows:
- Total chunks: 6,694
- Distribution by source
- Sample chunks

### Update Knowledge Base
To add new documents:
1. Place documents in `Data/` subdirectories
2. Run `python Code/Ingestion.py`
3. Run `python Code/VectorStore.py`

## 🚨 Troubleshooting

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
