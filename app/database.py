from flask_sqlalchemy import SQLAlchemy

# SQLAlchemyのインスタンスを作成
db = SQLAlchemy()

def init_db(app):
    # アプリにSQLAlchemyを設定
    db.init_app(app)

    # アプリケーションコンテキスト内でテーブルを作成
    with app.app_context():
        from app.models.user import User # noqa: F401
        from app.models.todo import Todo # noqa: F401
        import app.models # noqa: F401
        db.create_all()
