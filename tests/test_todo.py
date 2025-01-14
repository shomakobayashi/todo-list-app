import pytest
from app import create_app, db
from app.models.todo import Todo

@pytest.fixture
def app():
    app = create_app()
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
    app.config['TESTING'] = True

    with app.app_context():
        db.create_all()
    yield app

@pytest.fixture
def client(app):
    return app.test_client()

def test_get_todos(client):
    response = client.get('/todos')
    assert response.status_code == 200
    assert response.json == []

def test_create_todo(client):
    data = {"title": "Test Task", "description": "Task description", "user_id": 1}
    response = client.post('/todos', json=data)
    assert response.status_code == 200
    assert response.json["title"] == "Test Task"

def test_update_todo(client):
    data = {"title": "Test Task", "description": "Task description", "user_id": 1}
    client.post('/todos', json=data)
    update_data = {"title": "Updated Task"}
    response = client.put('/todos/1', json=update_data)
    assert response.status_code == 200
    assert response.json["title"] == "Updated Task"

def test_delete_todo(client):
    data = {"title": "Test Task", "description": "Task description", "user_id": 1}
    client.post('/todos', json=data)
    response = client.delete('/todos/1')
    assert response.status_code == 200
    assert response.json["message"] == "Todo deleted"
