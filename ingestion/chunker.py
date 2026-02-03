from langchain_text_splitters import RecursiveCharacterTextSplitter
from backend.config import CHUNK_SIZE, CHUNK_OVERLAP

def chunk_text(text):
    splitter = RecursiveCharacterTextSplitter(
        chunk_size=CHUNK_SIZE,
        chunk_overlap=CHUNK_OVERLAP
    )
    return splitter.split_text(text)
