from app import create_app, db
from app.models import User, Friend

app = create_app()
with app.app_context():
    db.create_all()
    print("✅ User, Friend テーブルを作成しました")
