from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

import pytest

from app.app import app
from app.config import settings
from app.database import get_db, Base

# load_dotenv()

# SQLALCHEMY_DATABASE_URL = settings.database_url
# assert SQLALCHEMY_DATABASE_URL is not None, "database url is missing"

SQLALCHEMY_DATABASE_URL = f"postgresql+psycopg://{settings.db_uname}:{settings.db_pass}@{settings.db_host}/{settings.db_name}_test"

engine = create_engine(SQLALCHEMY_DATABASE_URL, echo=False)

TestingSessionLocal = sessionmaker(bind=engine, autoflush=False, expire_on_commit=False)


@pytest.fixture()
def session():
    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()


@pytest.fixture()
def client(session):
    def overrid_get_db():
        try:
            yield session
        finally:
            session.close()

    app.dependency_overrides[get_db] = overrid_get_db
    yield TestClient(app)
