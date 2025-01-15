import pytest
from werkzeug.security import generate_password_hash

from app import create_app
from app.database import db
from app.models import User


@pytest.fixture
def app():
    app = create_app()
    app.config['TESTING'] = True
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'  # テスト用にSQLiteのメモリDBを使用
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    with app.app_context():
        db.create_all()  # テスト用のテーブルを作成
        yield app

        db.session.remove()
        db.drop_all()  # テスト後にデータベースをクリーンアップ

@pytest.fixture
def client(app):
    return app.test_client()

@pytest.fixture
def create_user():
    def _create_user(username, email, password):
        user = User(
            username=username,
            email=email,
            password=generate_password_hash(password)
        )
        db.session.add(user)
        db.session.commit()
        return user
    return _create_user