from app.config import settings
from dotenv import load_dotenv

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, DeclarativeBase

load_dotenv()


SQLALCHEMY_DATABASE_URL = f"postgresql+psycopg://{settings.db_uname}:{settings.db_pass}@{settings.db_host}/{settings.db_name}"

# SQLALCHEMY_DATABASE_URL = settings.database_url
# assert SQLALCHEMY_DATABASE_URL is not None, "database url is missing"

engine = create_engine(SQLALCHEMY_DATABASE_URL, echo=False)

SessionLocal = sessionmaker(bind=engine, autoflush=False, expire_on_commit=False)


class Base(DeclarativeBase):
    pass


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
