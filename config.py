import os

BASE_DIR = os.path.abspath(os.path.dirname(__file__))

class Config:
    # Render 環境では DATABASE_URL が設定されている
    uri = os.environ.get("DATABASE_URL")
    if uri:
        # postgres:// → postgresql+psycopg:// に変換
        if uri.startswith("postgres://"):
            uri = uri.replace("postgres://", "postgresql+psycopg://", 1)
        elif uri.startswith("postgresql://"):
            uri = uri.replace("postgresql://", "postgresql+psycopg://", 1)
        SQLALCHEMY_DATABASE_URI = uri
    else:
        # ローカル環境では SQLite を使用
        SQLALCHEMY_DATABASE_URI = "sqlite:///" + os.path.join(BASE_DIR, "dogfeed.db")

    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SECRET_KEY = os.environ.get("SECRET_KEY", "change-this-in-production")
