from flask import Flask
from app.database import db, init_db
from app.routes.todo.routes import todo_blueprint
from app.auth.routes import auth_blueprint
from dotenv import load_dotenv

def create_app():
    # Todo 認証情報をAWS Secretsへ移動する
    # .envファイルを読み込む
    # load_dotenv()

    app = Flask(__name__)

    # データベースURIの設定　Todo
    app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:password@localhost/todo_list'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    # Blueprint 登録
    app.register_blueprint(todo_blueprint)
    app.register_blueprint(auth_blueprint)

    # データベース初期化
    init_db(app)

    return app
