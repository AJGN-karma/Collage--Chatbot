from langchain_community.vectorstores import Chroma
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_huggingface import HuggingFaceEndpoint
from backend.prompt import SYSTEM_PROMPT
from backend.config import CHROMA_PATH, TOP_K, HF_API_TOKEN

embeddings = HuggingFaceEmbeddings(
    model_name="sentence-transformers/all-MiniLM-L6-v2"
)

vectordb = Chroma(
    persist_directory=CHROMA_PATH,
    embedding_function=embeddings
)

llm = HuggingFaceEndpoint(
    repo_id="HuggingFaceH4/zephyr-7b-beta",
    huggingfacehub_api_token=HF_API_TOKEN,
    temperature=0.1
)

def answer_question(question, history=""):
    docs = vectordb.similarity_search(question, k=TOP_K)
    context = "\n\n".join([d.page_content for d in docs])

    prompt = SYSTEM_PROMPT.format(
        context=context,
        history=history,
        question=question
    )

    return llm.invoke(prompt)
