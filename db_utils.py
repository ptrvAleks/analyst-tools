import sqlalchemy
from sqlalchemy.orm import sessionmaker

# Пример для PostgreSQL:
DATABASE_URL = "postgresql://user:password@localhost:5432/your_db_name"

engine = sqlalchemy.create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


def get_db_session():
    """
    Возвращает сессию SQLAlchemy. Используйте внутри функций:

        with get_db_session() as session:
            # работать с session
    """
    session = SessionLocal()
    try:
        yield session
    finally:
        session.close()