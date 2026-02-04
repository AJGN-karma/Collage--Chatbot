from langchain_community.vectorstores import Chroma
from langchain_huggingface import HuggingFaceEmbeddings
from transformers import pipeline

from backend.prompt import SYSTEM_PROMPT
from backend.config import CHROMA_PATH, TOP_K
from backend.memory import get_chat_history, save_message

# -------------------------------------------------
# Embedding Model (LOCKED)
# -------------------------------------------------
embeddings = HuggingFaceEmbeddings(
    model_name="sentence-transformers/all-MiniLM-L6-v2"
)

# -------------------------------------------------
# Vector Database (LOCKED)
# -------------------------------------------------
vectordb = Chroma(
    persist_directory=CHROMA_PATH,
    embedding_function=embeddings
)

# -------------------------------------------------
# Local LLM (LOCKED, STABLE, CPU)
# -------------------------------------------------
llm = pipeline(
    "text2text-generation",
    model="google/flan-t5-base",
    device=-1  # CPU
)


def generate_text(prompt: str) -> str:
    """
    Deterministic local text generation.
    Hard constrained to avoid repetition and hallucination.
    """
    result = llm(
        prompt,
        max_new_tokens=128,
        do_sample=False,
        repetition_penalty=1.2,
        no_repeat_ngram_size=3
    )
    return result[0]["generated_text"].strip()


def answer_question(question: str, user_id: str) -> str:
    """
    FINAL RAG PIPELINE (LOCKED)

    Flow:
    1. Load conversation memory (Firestore)
    2. Retrieve relevant document chunks (Chroma)
    3. Assemble strict prompt
    4. Generate local LLM answer
    5. Save conversation history
    """

    # 1. Load conversation memory (fail-safe)
    history = get_chat_history(user_id)

    # 2. Retrieve documents
    docs = vectordb.similarity_search(question, k=TOP_K)
    context = "\n\n".join(d.page_content for d in docs)

    # 3. Build prompt
    prompt = SYSTEM_PROMPT.format(
        context=context,
        history=history,
        question=question
    )

    # 4. Generate answer
    answer = generate_text(prompt)

    # 5. Hard fallback safety (demo-proof)
    if not answer or len(answer.split()) > 80:
        answer = "The requested information is not available in the college records."

    # 6. Save conversation (fire-and-forget)
    save_message(user_id, "user", question)
    save_message(user_id, "assistant", answer)

    return answer
