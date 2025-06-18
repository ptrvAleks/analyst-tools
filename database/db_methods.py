from firebase_admin import firestore
from datetime import datetime, timedelta, timezone
from database.db import db

MSK = timezone(timedelta(hours=3))  # Москва — UTC+3


def save_conversion(uid, result):
    db.collection("users").document(uid).collection("conversions").add({
        "converted": result,
        "timestamp": datetime.now(MSK)
    })

def get_conversions(uid):
    docs = db.collection("users").document(uid).collection("conversions") \
    .order_by("timestamp", direction=firestore.Query.DESCENDING).stream()

    return [{"id": doc.id, **doc.to_dict()} for doc in docs]

def delete_conversion(uid, document_id):
    db.collection("users").document(uid).collection("conversions").document(document_id).delete()