from firebase_admin import firestore
from datetime import datetime, timedelta, timezone
from database.db import db
from google.cloud import firestore as gcfirestore


MSK = timezone(timedelta(hours=3))  # Москва — UTC+3


def save_conversion(uid, result):
    db.collection("users").document(uid).collection("conversions").add({
        "converted": result,
        "timestamp": datetime.now(MSK)
    })

def get_conversions(uid):
    docs = firestore.client().collection("users").document(uid).collection("conversions") \
        .order_by("timestamp", direction=gcfirestore.Query.DESCENDING).stream()

    return [{"id": doc.id, **doc.to_dict()} for doc in docs]

def delete_conversion(uid, document_id):
    db.collection("users").document(uid).collection("conversions").document(document_id).delete()

def delete_user_data(uid: str):
    user_ref = db.collection("users").document(uid)
    conversions_ref = user_ref.collection("conversions").stream()

    # Удаляем все документы в подколлекции "conversions"
    for doc in conversions_ref:
        user_ref.collection("conversions").document(doc.id).delete()

    # Удаляем сам документ пользователя
    user_ref.delete()