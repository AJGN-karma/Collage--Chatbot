import firebase_admin
from firebase_admin import credentials, firestore

if not firebase_admin._apps:
    cred = credentials.Certificate("firebase_key.json")
    firebase_admin.initialize_app(cred)

db = firestore.client()

MAX_HISTORY = 6
def get_chat_history(user_id: str) -> str:
    docs = (
        db.collection("chat_history")
        .document(user_id)
        .collection("messages")
        .order_by("timestamp")
        .limit_to_last(MAX_HISTORY)
        .stream()
    )

    history = []
    for d in docs:
        data = d.to_dict()
        history.append(f"{data['role']}: {data['content']}")

    return "\n".join(history)


def save_message(user_id: str, role: str, content: str):
    db.collection("chat_history") \
      .document(user_id) \
      .collection("messages") \
      .add({
          "role": role,
          "content": content,
          "timestamp": firestore.SERVER_TIMESTAMP
      })
