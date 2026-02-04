from backend.rag import answer_question

user_id = "test_user_001"

print("Q1:")
print(answer_question("What courses are offered?", user_id))

print("\nQ2:")
print(answer_question("What is the duration?", user_id))
