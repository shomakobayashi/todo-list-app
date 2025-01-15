from flask import request, jsonify
from functools import wraps
from app.utils.jwt_helper import decode_jwt

def jwt_required(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        auth_header = request.headers.get("Authorization")
        if not auth_header or not auth_header.startswith("Bearer "):
            return jsonify({"error": "Authorization token is missing"}), 401

        token = auth_header.split(" ")[1]
        payload = decode_jwt(token)

        if "error" in payload:
            return jsonify({"error": payload["error"]}), 401

        request.user_id = payload["user_id"]  # デコードしたユーザーIDをリクエストに追加
        return func(*args, **kwargs)

    return wrapper
