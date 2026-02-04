from backend.memory import db

doc_ref = db.collection("test").document("ping")
doc_ref.set({"status": "ok"})

print("Firebase connection successful")
