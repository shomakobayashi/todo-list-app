import jwt
import datetime

SECRET_KEY = "your_secret_key"  # 適切なシークレットキーを設定

def create_jwt(user_id):
    """
    JWTトークンを生成
    """
    payload = {
        "user_id": user_id,
        "exp": datetime.datetime.utcnow() + datetime.timedelta(hours=1)  # 1時間で期限切れ
    }
    token = jwt.encode(payload, SECRET_KEY, algorithm="HS256")
    return token

def decode_jwt(token):
    """
    JWTトークンをデコード
    """
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=["HS256"])
        return payload
    except jwt.ExpiredSignatureError:
        return {"error": "Token has expired"}
    except jwt.InvalidTokenError:
        return {"error": "Invalid token"}
