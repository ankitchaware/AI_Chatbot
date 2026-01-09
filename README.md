# RAG-Based Chatbot with Context Optimization

A Retrieval-Augmented Generation chatbot that answers questions from uploaded PDFs while maintaining conversation context for up to 50 consecutive user queries.

## Features
- PDF ingestion with chunking
- FAISS vector store
- Groq-powered LLM (Llama3-70b) for fast responses
- Long context memory (up to ~50 turns)
- Streamlit web interface

## Setup Instructions
1. Clone the repo
2. Create `.env` file with `GROQ_API_KEY=your_key` (for LLM responses - get free key from https://console.groq.com/)
3. `pip install -r requirements.txt`
4. Place PDFs in `Data/raw_pdfs/`
5. Run ingestion: `python backend/ingest.py` (from project root directory)
6. Launch app: `streamlit run frontend/app.py`

**Note:** This project uses HuggingFace embeddings (free, no API key required) for vector search. Only Groq API key is needed for LLM responses.

## Usage
- First run ingestion whenever you add new PDFs
- Chat in the web UI — the bot remembers previous questions/answers