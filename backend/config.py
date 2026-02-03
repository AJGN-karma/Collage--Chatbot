import os

# HuggingFace
HF_API_TOKEN = os.getenv("HF_API_TOKEN")

# Vector DB
CHROMA_PATH = "data/vectordb"

# RAG
TOP_K = 4
CHUNK_SIZE = 400
CHUNK_OVERLAP = 50
