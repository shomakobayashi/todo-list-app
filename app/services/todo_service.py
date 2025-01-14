from flask import jsonify
from app.models.todo import Todo
from app.database import db

class TodoService:
    @staticmethod
    def get_all_todos():
        todos = db.session.query(Todo).all()
        return jsonify([todo.serialize() for todo in todos])

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

    @staticmethod
    def update_todo(todo_id, data):
        todo = db.session.query(Todo).filter_by(id=todo_id).first()
        if not todo:
            return jsonify({'error': 'Todo not found'}), 404

        # フィールドの更新
        todo.title = data.get('title', todo.title)
        todo.description = data.get('description', todo.description)

        #データベースにコミット
        db.session.commit()

        return jsonify(todo.serialize())

    @staticmethod
    def delete_todo(todo_id):
        todo = db.session.query(Todo).filter_by(id=todo_id).first()
        if not todo:
            return jsonify({'error': 'Todo not found'}), 404
        db.session.delete(todo)
        db.session.commit()
        return jsonify({'message': 'Todo deleted'})
