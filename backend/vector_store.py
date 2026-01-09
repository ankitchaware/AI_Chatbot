import os
from pathlib import Path
from langchain_community.vectorstores import FAISS

BASE_DIR = Path(__file__).resolve().parent.parent

try:
    from langchain_huggingface import HuggingFaceEmbeddings
    print("Using langchain-huggingface package (recommended)")
except ImportError:
    try:
        from langchain_community.embeddings import HuggingFaceEmbeddings
        print("Using langchain_community.embeddings (deprecated, consider installing langchain-huggingface)")
    except ImportError:
        raise ImportError(
            "Neither langchain-huggingface nor langchain_community.embeddings found. "
            "Please install: pip install langchain-huggingface"
        )

try:
    embedding_model = HuggingFaceEmbeddings(
        model_name="sentence-transformers/all-MiniLM-L6-v2",
        model_kwargs={'device': 'cpu'},
        encode_kwargs={'normalize_embeddings': True}
    )
    test_embedding = embedding_model.embed_query("test")

    print(f"[OK] HuggingFace embeddings initialized successfully (dimension: {len(test_embedding)})")
except Exception as e:
    error_msg = str(e)
    if "sentence_transformers" in error_msg.lower() or "sentence-transformers" in error_msg.lower():
        raise ImportError(
            f"Failed to load sentence-transformers: {error_msg}\n"
            "Please install it with: pip install sentence-transformers"
        )
    else:
        raise RuntimeError(
            f"Failed to initialize HuggingFace embeddings: {error_msg}\n"
            "Please ensure sentence-transformers is installed: pip install sentence-transformers"
        )


def create_vector_store(chunks):
    if not chunks:
        raise ValueError("Cannot create vector store: no chunks provided.")
    vector_store = FAISS.from_texts(chunks, embedding_model)
    return vector_store


def save_vector_store(vector_store, folder=None):
    if folder is None:
        folder = BASE_DIR / "Data" / "processed"
    else:
        folder = Path(folder)
    folder.mkdir(parents=True, exist_ok=True)
    vector_store.save_local(str(folder))


def load_vector_store(folder=None):
    if folder is None:
        folder = BASE_DIR / "Data" / "processed"
    else:
        folder = Path(folder)
    
    index_path = folder / "index.faiss"
    if not index_path.exists():
        raise FileNotFoundError(f"Vector store not found at '{folder}'. Run ingestion first.")
    return FAISS.load_local(str(folder), embedding_model, allow_dangerous_deserialization=True)