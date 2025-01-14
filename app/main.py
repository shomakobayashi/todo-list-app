from app import create_app

# アプリケーションを作成
app = create_app()

if __name__ == "__main__":
    # Flaskアプリをデバッグモードで実行
    app.run(debug=True)