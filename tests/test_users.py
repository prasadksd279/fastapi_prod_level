import jwt
from app import schemas
from app.config import settings
import pytest


def test_root(client):
    res = client.get("/")
    print(res.json().get("hello"))
    assert res.json().get("hello") == "worlds of both"
    assert res.status_code == 200


def test_create_user(client, test_user):
    res = client.post(
        "/users", json={"email": "test@email.com", "password": "testpass@123"}
    )
    assert res.status_code == 201
    new_user = schemas.UserOut.model_validate(res.json())
    assert new_user.email == "test@email.com"


def test_login_user(client, test_user):
    res = client.post(
        "/login",
        data={"username": test_user["email"], "password": test_user["password"]},
    )
    login_res = schemas.Token.model_validate(res.json())
    payload = jwt.decode(
        login_res.access_token, settings.secret_key, algorithms=[settings.algorithm]
    )
    id = payload.get("user_id")
    assert id == test_user["id"]
    assert login_res.token_type == "bearer"
    assert res.status_code == 200


@pytest.mark.parametrize(
    "email, password, status_code",
    [
        ("wrongemail@email.com", "testpass@123", 403),
        ("test@email.com", "testpass@123", 403),
        ("wrongemail@email.com", "wrong password", 403),
        (None, "testpass@123", 403),
        ("test@email.com", None, 403),
    ],
)
def test_incorrect_login(test_user, client, email, password, status_code):
    res = client.post(
        "/login",
        data={"username": email, "password": password},
    )
    assert res.status_code == status_code
    # assert res.json().get("detail") == "Invalid Credentials"
