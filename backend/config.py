import os
from dotenv import load_dotenv

load_dotenv()

HF_API_TOKEN = os.getenv("HF_API_TOKEN")

CHROMA_PATH = "data/vectordb"
TOP_K = 4

CHUNK_SIZE = 400
CHUNK_OVERLAP = 50
