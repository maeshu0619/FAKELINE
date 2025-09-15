from flask import Flask
from config import Config
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    db.init_app(app)

    with app.app_context():
        # モデルを import してテーブル作成
        from . import models
        db.create_all()

    from .routes import bp as main_bp
    app.register_blueprint(main_bp)

    return app
