from flask import Blueprint, request, jsonify
from werkzeug.security import check_password_hash
from app.models.user import User
from app.database import db
from app.utils.jwt_helper import create_jwt

# 認証関連のルートを管理するBlueprintを作成
auth_blueprint = Blueprint('auth', __name__, url_prefix='/auth')

# ログイン処理
@auth_blueprint.route('/login', methods=['POST'])
def login():
    # クライアントから送信されたJSONデータを取得
    data = request.json
    # usernameに基づいてデータベースからユーザーを検索
    user = db.session.query(User).filter_by(username=data['username']).first()

    if user and check_password_hash(user.password, data['password']):
        token = create_jwt(user.id)
        return jsonify({"access_token": token}), 200
    return jsonify({"error": "Invalid credentials"}), 401
