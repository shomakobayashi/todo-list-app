# from flask import Blueprint, request, jsonify
# import boto3
# import os
#
# auth_blueprint = Blueprint('auth', __name__)
#
# # Cognito設定
# COGNITO_REGION = os.getenv("COGNITO_REGION", "ap-northeast-1")
# COGNITO_CLIENT_ID = os.getenv("COGNITO_CLIENT_ID")
# COGNITO_CLIENT_SECRET = os.getenv("COGNITO_CLIENT_SECRET")
#
# # Cognitoクライアント
# cognito_client = boto3.client('cognito-idp', region_name=COGNITO_REGION)
#
# @auth_blueprint.route('/', methods=['GET'])
# def login_page():
#     return jsonify({"message": "Welcome to the login page. Please use POST to authenticate."})
#
# @auth_blueprint.route('/', methods=['POST'])
# def login():
#     try:
#         # リクエストデータを取得
#         data = request.json
#         username = data.get('username')
#         password = data.get('password')
#
#         if not username or not password:
#             return jsonify({"error": "Username and password are required"}), 400
#
#         # Cognitoで認証
#         response = cognito_client.initiate_auth(
#             ClientId=COGNITO_CLIENT_ID,
#             AuthFlow='USER_PASSWORD_AUTH',
#             AuthParameters={
#                 'USERNAME': username,
#                 'PASSWORD': password
#             }
#         )
#
#         # トークンを返す
#         return jsonify({
#             "message": "Login successful",
#             "id_token": response['AuthenticationResult']['IdToken'],
#             "access_token": response['AuthenticationResult']['AccessToken'],
#             "refresh_token": response['AuthenticationResult']['RefreshToken']
#         })
#     except cognito_client.exceptions.NotAuthorizedException:
#         return jsonify({"error": "Invalid username or password"}), 401
#     except cognito_client.exceptions.UserNotFoundException:
#         return jsonify({"error": "User does not exist"}), 404
#     except Exception as e:
#         return jsonify({"error": str(e)}), 500
