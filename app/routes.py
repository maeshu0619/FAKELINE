import os
from flask import Blueprint, render_template, redirect, url_for, current_app
from .models import Feed, Trash
from . import db
import datetime

bp = Blueprint("main", __name__)

DOGS = ["てつ", "ぽんず"]
TIMES = ["朝", "昼", "夜"]

@bp.route("/initdb")
def initdb():
    db.create_all()
    return "✅ Tables created"

@bp.route("/")
def index():
    # 初回アクセス時にテーブルを作成
    db.create_all()

    today = datetime.date.today().isoformat()

    # 今日のレコードが無ければ初期化
    for dog in DOGS:
        for t in TIMES:
            if not Feed.query.filter_by(date=today, dog=dog, time=t).first():
                db.session.add(Feed(date=today, dog=dog, time=t, fed=False))
    if not Trash.query.filter_by(date=today).first():
        db.session.add(Trash(date=today, taken=False))
    db.session.commit()

    feeds = Feed.query.filter_by(date=today).all()
    trash = Trash.query.filter_by(date=today).first()
    state = {(f.dog, f.time): f.fed for f in feeds}

    # === ここを追加 ===
    friends_dir = os.path.join(current_app.static_folder, "images", "friends")
    friend_files = []
    if os.path.exists(friends_dir):
        friend_files = [
            os.path.splitext(f)[0]
            for f in os.listdir(friends_dir)
            if os.path.isfile(os.path.join(friends_dir, f))
            and os.path.splitext(f)[1].lower() in [".png", ".jpg", ".jpeg"]
        ]
    # ==================

    return render_template(
        "index.html",
        today=today,
        state=state,
        DOGS=DOGS,
        TIMES=TIMES,
        trash=trash.taken,
        friend_files=friend_files   # ← 追加
    )
@bp.route("/toggle/<dog>/<time>")
def toggle(dog, time):
    today = datetime.date.today().isoformat()
    feed = Feed.query.filter_by(date=today, dog=dog, time=time).first()
    feed.fed = not feed.fed
    db.session.commit()
    return redirect(url_for("main.index"))

@bp.route("/toggle_trash")
def toggle_trash():
    today = datetime.date.today().isoformat()
    trash = Trash.query.filter_by(date=today).first()
    trash.taken = not trash.taken
    db.session.commit()
    return redirect(url_for("main.index"))
