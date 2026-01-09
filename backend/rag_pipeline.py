from langchain_groq import ChatGroq
from backend.vector_store import load_vector_store
from dotenv import load_dotenv
import os

load_dotenv()

groq_api_key = os.getenv("GROQ_API_KEY")
if not groq_api_key:
    raise ValueError(
        "GROQ_API_KEY not found in environment variables. "
        "Please create a .env file with GROQ_API_KEY=your_key"
    )

llm = ChatGroq(
    model_name="llama-3.3-70b-versatile",
    temperature=0.7,
    groq_api_key=groq_api_key,
)

try:
    vector_store = load_vector_store()
    retriever = vector_store.as_retriever(search_kwargs={"k": 4})
except FileNotFoundError as e:
    raise FileNotFoundError(
        f"{e}\nPlease run 'python backend/ingest.py' first to create the vector store."
    )


def _build_context(question: str) -> str:
    """Retrieve relevant documents and concatenate their content into a context string."""
    try:
        docs = retriever.invoke(question)
    except (AttributeError, TypeError):
        try:
            docs = retriever.get_relevant_documents(question)
        except AttributeError:
            docs = vector_store.similarity_search(question, k=4)
    
    if not docs:
        return ""
    if isinstance(docs[0], str):
        return "\n\n".join(docs)
    else:
        return "\n\n".join(doc.page_content for doc in docs)


def get_response(question: str) -> str:
    """Simple RAG pipeline: retrieve, then ask Groq LLM with a formatted prompt."""
    context = _build_context(question)
    prompt = (
        "You are an intelligent assistant. Answer the question based only on the "
        "following context:\n"
        f"{context}\n\n"
        f"Question: {question}\n"
        'If you do not know the answer, say "I do not have information about that '
        'in the provided documents."\n\n'
        "Answer:"
    )
    result = llm.invoke(prompt)
    return getattr(result, "content", str(result))