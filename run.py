from app import create_app

app = create_app()

if __name__ == "__main__":
    # 開発用サーバ
    app.run(debug=True)
