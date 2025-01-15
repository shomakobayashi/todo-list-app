import json
from app.models.todo import Todo
from app.models.user import User
from app.database import db
from werkzeug.security import generate_password_hash
from app.utils.jwt_helper import create_jwt

def test_get_todos_empty(client):
    # テスト用ユーザーを作成
    user = User(username="testuser", password=generate_password_hash("password"))
    db.session.add(user)
    db.session.commit()

    # ユーザーのトークンを生成
    token = create_jwt(user.id)

    # タスクリストを取得
    response = client.post(
        "/todos",
        headers={"Authorization": f"Bearer {token}"},
    )

    assert response.status_code == 200
    assert response.get_json() == []  # 空のリストを期待

def test_create_todo_success(client):
    # テスト用ユーザーを作成
    user = User(username="testuser", password=generate_password_hash("password"))
    db.session.add(user)
    db.session.commit()

    # ユーザーのトークンを生成

    token = create_jwt(user.id)

    # 新しいタスクを作成
    response = client.post(
        "/todos",
        headers={"Authorization": f"Bearer {token}"},
        data=json.dumps({"title": "Test Todo", "description": "This is a test todo."}),
        content_type="application/json",
    )

    assert response.status_code == 200
    todo = response.get_json()
    assert todo["title"] == "Test Todo"
    assert todo["description"] == "This is a test todo."
    assert todo["user_id"] == user.id

    def test_get_todos_with_data(client):
        user = User(username="testuser", password=generate_password_hash("password"))
        db.session.add(user)
        db.session.commit()
        token = create_jwt(user.id)

        todo1 = Todo(title="Task 1", description="First task", user_id=user.id)
        todo2 = Todo(title="Task 2", description="Second task", user_id=user.id)
        db.session.add_all([todo1, todo2])
        db.session.commit()

        response = client.post(
            "/todos",
            headers={"Authorization": f"Bearer {token}"},
        )

        todos = response.get_json()
        assert response.status_code == 200
        assert len(todos) == 2

    def test_update_todo_not_found(client):
        user = User(username="testuser", password=generate_password_hash("password"))
        db.session.add(user)
        db.session.commit()
        token = create_jwt(user.id)

        response = client.put(
            "/todos/999",  # 存在しないタスクID
            headers={"Authorization": f"Bearer {token}"},
            data=json.dumps({"title": "Updated Task"}),
            content_type="application/json",
        )

        assert response.status_code == 404
        assert response.get_json() == {"error": "Todo not found or unauthorized"}

def test_update_other_user_todo(client):
    user1 = User(username="user1", password=generate_password_hash("password"))
    user2 = User(username="user2", password=generate_password_hash("password"))
    db.session.add_all([user1, user2])
    db.session.commit()

    todo = Todo(title="Task 1", description="User 1 task", user_id=user1.id)
    db.session.add(todo)
    db.session.commit()

    token = create_jwt(user2.id)

    response = client.put(
        f"/todos/{todo.id}",
        headers={"Authorization": f"Bearer {token}"},
        data=json.dumps({"title": "Updated Task"}),
        content_type="application/json",
    )

    assert response.status_code == 404
    assert response.get_json() == {"error": "Todo not found or unauthorized"}

