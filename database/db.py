import firebase_admin
from firebase_admin import firestore, credentials
from database.config import get_firebase_config
from environments import get_environment

env = get_environment()
cred = credentials.Certificate(get_firebase_config(env))
firebase_admin.initialize_app(cred)

db = firestore.client()

print(f"✅ Firebase подключен — среда: {get_environment()}")