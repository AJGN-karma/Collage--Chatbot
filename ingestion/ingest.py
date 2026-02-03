from langchain_huggingface import HuggingFaceEmbeddings
from langchain_community.vectorstores import Chroma
from ingestion.loader import load_pdf
from ingestion.chunker import chunk_text
from backend.config import CHROMA_PATH


embeddings = HuggingFaceEmbeddings(
    model_name="sentence-transformers/all-MiniLM-L6-v2"
)

def ingest(pdf_path):
    text = load_pdf(pdf_path)
    chunks = chunk_text(text)

    vectordb = Chroma(
        persist_directory=CHROMA_PATH,
        embedding_function=embeddings
    )

    vectordb.add_texts(chunks)
    vectordb.persist()

if __name__ == "__main__":
    ingest("data/raw_docs/sample.pdf")
