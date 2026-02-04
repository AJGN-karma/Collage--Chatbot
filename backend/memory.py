import firebase_admin
from firebase_admin import credentials, firestore

# Initialize Firebase Admin SDK (ONLY ONCE)
if not firebase_admin._apps:
    cred = credentials.Certificate("firebase_key.json")
    firebase_admin.initialize_app(cred)

# Firestore client
db = firestore.client()

# Max number of past messages to keep as conversation memory
MAX_HISTORY = 6


def get_chat_history(user_id: str) -> str:
    """
    Fetch last N chat messages for a user.
    Used ONLY for conversational context (not knowledge).
    Fail-safe: returns empty string if anything goes wrong.
    """
    try:
        query = (
            db.collection("chat_history")
            .document(user_id)
            .collection("messages")
            .order_by("timestamp")
            .limit(MAX_HISTORY)
        )

        docs = query.get()

        history = []
        for d in docs:
            data = d.to_dict()
            history.append(f"{data['role']}: {data['content']}")

        return "\n".join(history)

    except Exception as e:
        # Memory must NEVER break the chatbot
        print("[MEMORY READ FAILED]", e)
        return ""


def save_message(user_id: str, role: str, content: str):
    """
    Save a single chat message.
    Fire-and-forget: failure does NOT affect chatbot response.
    """
    try:
        db.collection("chat_history") \
          .document(user_id) \
          .collection("messages") \
          .add({
              "role": role,
              "content": content,
              "timestamp": firestore.SERVER_TIMESTAMP
          })
    except Exception as e:
        print("[MEMORY WRITE FAILED]", e)
