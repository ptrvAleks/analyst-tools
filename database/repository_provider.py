# repository_provider.py
from database.i_user_repository import IUserRepository
from database.firestore_user_repository import FirestoreUserRepository

def get_user_repository() -> IUserRepository:
    # 🟢 Меняется только это при переходе на PostgreSQL
    return FirestoreUserRepository()