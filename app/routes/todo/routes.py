from flask import Blueprint, request, jsonify
from app.services.todo_service import TodoService

todo_blueprint = Blueprint('todo', __name__, url_prefix='/todos')

# @todo_blueprint.route('/', methods=['GET'])
# def home():
#     return "Welcome to the Todo API!"

@todo_blueprint.route('', methods=['GET'])
def get_todos():
    return TodoService.get_all_todos()

@todo_blueprint.route('', methods=['POST'])
def create_todo():
    data = request.json
    return TodoService.create_todo(data)

@todo_blueprint.route('/<int:todo_id>', methods=['PUT'])
def update_todo(todo_id):
    data = request.json
    return TodoService.update_todo(todo_id, data)

@todo_blueprint.route('/<int:todo_id>', methods=['DELETE'])
def delete_todo(todo_id):
    return TodoService.delete_todo(todo_id)
