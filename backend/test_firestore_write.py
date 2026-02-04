import firebase_admin
from firebase_admin import credentials, firestore

cred = credentials.Certificate("firebase_key.json")
firebase_admin.initialize_app(cred)

db = firestore.client()

db.collection("chat_history") \
  .document("firestore_test_user") \
  .collection("messages") \
  .add({
      "role": "system",
      "content": "firestore write test",
      "timestamp": firestore.SERVER_TIMESTAMP
  })

print("WRITE COMPLETE")
