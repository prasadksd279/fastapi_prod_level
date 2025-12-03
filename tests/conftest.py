from fastapi.testclient import TestClient
from sqlalchemy import create_engine, select
from sqlalchemy.orm import sessionmaker

import pytest

from app.app import app
from app.config import settings
from app.database import get_db, Base
from app import models
from app.oauth2 import create_access_token

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


@pytest.fixture
def test_user2(client):
    user_data = {"email": "testuser2@email.com", "password": "testpass"}
    res = client.post("/users/", json=user_data)
    assert res.status_code == 201
    new_user = res.json()
    new_user["password"] = user_data["password"]
    return new_user


@pytest.fixture
def test_user(client):
    user_data = {"email": "testuser@email.com", "password": "testpass"}
    res = client.post("/users/", json=user_data)
    assert res.status_code == 201
    new_user = res.json()
    new_user["password"] = user_data["password"]
    return new_user


@pytest.fixture
def token(test_user):
    return create_access_token({"user_id": test_user["id"]})


@pytest.fixture
def authorized_client(client, token):
    client.headers = {**client.headers, "authorization": f"Bearer {token}"}

    return client


@pytest.fixture
def test_posts(test_user, session, test_user2):
    posts_data = [
        {
            "title": "first title",
            "content": "first content",
            "owner_id": test_user["id"],
        },
        {
            "title": "second title",
            "content": "second content",
            "owner_id": test_user["id"],
        },
        {
            "title": "third title",
            "content": "third content",
            "owner_id": test_user["id"],
        },
        {
            "title": "third title",
            "content": "third content",
            "owner_id": test_user2["id"],
        },
    ]

    def create_post_model(post):
        return models.Post(**post)

    post_map = map(create_post_model, posts_data)
    posts = list(post_map)
    session.add_all(posts)
    session.commit()
    # session.query(models.Post).all()
    stmnt = select(models.Post)
    posts = session.execute(stmnt).scalars().all()
    return posts
