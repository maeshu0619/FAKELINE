import os

BASE_DIR = os.path.abspath(os.path.dirname(__file__))

class Config:
    # プロジェクト直下に dogfeed.db を置く
    DB_PATH = os.path.join(BASE_DIR, "dogfeed.db")
    SECRET_KEY = "change-this-in-production"


# import os

# class Config:
#     uri = os.environ.get("DATABASE_URL")
#     if uri and uri.startswith("postgres://"):
#         uri = uri.replace("postgres://", "postgresql+psycopg://", 1)
#     elif uri and uri.startswith("postgresql://"):
#         uri = uri.replace("postgresql://", "postgresql+psycopg://", 1)

#     SQLALCHEMY_DATABASE_URI = uri
#     SQLALCHEMY_TRACK_MODIFICATIONS = False
#     SECRET_KEY = os.environ.get("SECRET_KEY", "change-me")
