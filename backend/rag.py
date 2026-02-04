from backend.memory import get_chat_history, save_message

def answer_question(question: str, user_id: str):
    history = get_chat_history(user_id)

    docs = vectordb.similarity_search(question, k=TOP_K)
    context = "\n\n".join([d.page_content for d in docs])

    prompt = SYSTEM_PROMPT.format(
        context=context,
        history=history,
        question=question
    )

    answer = llm.invoke(prompt)

    save_message(user_id, "user", question)
    save_message(user_id, "assistant", answer)

    return answer
