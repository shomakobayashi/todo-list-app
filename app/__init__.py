from flask import Flask
from app.database import db, init_db
from app.routes.todo.routes import todo_blueprint
# from app.auth.routes import auth_blueprint

def create_app():
    app = Flask(__name__)

    # Cognitoの設定（環境変数を使用）
    app.config['COGNITO_REGION'] = 'ap-northeast-1'
    app.config['COGNITO_CLIENT_ID'] = '<YourClientId>'
    app.config['COGNITO_CLIENT_SECRET'] = '<YourClientSecret>'

    # データベースURIの設定
    app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:password@localhost/todo_list'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    # Blueprint 登録
    app.register_blueprint(todo_blueprint)
    # app.register_blueprint(auth_blueprint)

    # データベース初期化
    init_db(app)

    return app
