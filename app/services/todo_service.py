from flask import jsonify
from app.models.todo import Todo
from app.database import db

class TodoService:

    # ユーザーIDに紐づくすべてのタスクを取得
    @staticmethod
    def get_all_todos(user_id):
        todos = db.session.query(Todo).filter_by(user_id=user_id).all()  # 指定されたユーザーIDに紐づくタスクを取得
        return jsonify([todo.serialize() for todo in todos])

    # 新しいタスクを作成
    @staticmethod
    def create_todo(data):
        todo = Todo(
            title=data.get('title'),
            description=data.get('description'),
            user_id=data.get('user_id')
        )

        db.session.add(todo)
        db.session.commit()

        return jsonify(todo.serialize())

    # 指定されたタスクを更新
    @staticmethod
    def update_todo(todo_id, user_id, data):
        todo = db.session.query(Todo).filter_by(id=todo_id, user_id=user_id).first()

        if not todo:
            return jsonify({'error': 'Todo not found or unauthorized'}), 404

        todo.title = data.get('title', todo.title)
        todo.description = data.get('description', todo.description)
        db.session.commit()

        return jsonify(todo.serialize())

    # 指定されたタスクを削除
    @staticmethod
    def delete_todo(todo_id, user_id):
        todo = db.session.query(Todo).filter_by(id=todo_id, user_id=user_id).first()

        if not todo:
            return jsonify({'error': 'Todo not found or unauthorized'}), 404

        db.session.delete(todo)
        db.session.commit()

        return jsonify({'message': 'Todo deleted'})
