import json
from app.models.user import User
from app.database import db
from werkzeug.security import generate_password_hash

def test_login_success(client, create_user):
    # テスト用ユーザーを作成
    create_user("testuser", "testuser@example.com", "password")

    response = client.post(
        "/auth/login",
        data=json.dumps({"username": "testuser", "password": "password"}),
        content_type="application/json",
    )

    assert response.status_code == 200
    assert "access_token" in response.get_json()


def test_login_failure(client):
    # 存在しないユーザーでログインを試みる
    response = client.post(
        "/auth/login",
        data=json.dumps({"username": "nonexistent", "password": "password"}),
        content_type="application/json",
    )

    assert response.status_code == 401
    assert response.get_json() == {"error": "Invalid credentials"}

def test_login_empty_request(client):
    response = client.post(
        "/auth/login",
        data=json.dumps({}),  # 空のデータ
        content_type="application/json",
    )
    assert response.status_code == 401
    assert response.get_json() == {"error": "Invalid credentials"}

def test_login_missing_fields(client):
    response = client.post(
        "/auth/login",
        data=json.dumps({"username": "testuser"}),  # パスワードが欠落
        content_type="application/json",
    )
    assert response.status_code == 401
    assert response.get_json() == {"error": "Invalid credentials"}
