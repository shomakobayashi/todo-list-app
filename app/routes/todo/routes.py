from flask import Blueprint, request, jsonify
from app.services.todo_service import TodoService
from app.middle.auth import jwt_required

# Blueprintを作成し、'/todos' というURLプレフィックスを設定
todo_blueprint = Blueprint('todo', __name__, url_prefix='/todos')

# タスクの取得
@todo_blueprint.route('', methods=['POST'])
@jwt_required # JWTトークンが必要で、認証されたユーザーのみアクセス可能
def get_todos():
    user_id = request.user_id # JWTから取得したユーザーIDを使用
    return TodoService.get_all_todos(user_id)

# タスクの作成
@todo_blueprint.route('', methods=['POST'])
@jwt_required
def create_todo():
    user_id = request.user_id
    data = request.json
    data['user_id'] = user_id
    return TodoService.create_todo(data)

# タスクの更新
@todo_blueprint.route('/<int:todo_id>', methods=['PUT'])
@jwt_required
def update_todo(todo_id):
    user_id = request.user_id
    data = request.json
    return TodoService.update_todo(todo_id, user_id, data)

# タスクの削除
@todo_blueprint.route('/<int:todo_id>', methods=['DELETE'])
@jwt_required
def delete_todo(todo_id):
    user_id = request.user_id
    return TodoService.delete_todo(todo_id, user_id)
