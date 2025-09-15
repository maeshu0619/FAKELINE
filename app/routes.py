import os
from flask import Blueprint, render_template, redirect, url_for, current_app, request, session, flash
from .models import User, Friend
from . import db

bp = Blueprint("main", __name__)

@bp.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]
        user = User.query.filter_by(username=username).first()
        if user and user.check_password(password):
            session["user_id"] = user.id
            return redirect(url_for("main.index"))
        flash("ログイン失敗")
    return render_template("login.html")

@bp.route("/logout")
def logout():
    session.pop("user_id", None)
    return redirect(url_for("main.login"))

@bp.route("/friends", methods=["GET", "POST"])
def friends():
    user_id = session.get("user_id")
    if not user_id:
        return redirect(url_for("main.login"))

    if request.method == "POST":
        if "delete_id" in request.form:  # 削除処理
            fid = request.form["delete_id"]
            friend = Friend.query.filter_by(id=fid, user_id=user_id).first()
            if friend:
                db.session.delete(friend)
                db.session.commit()
            return redirect(url_for("main.friends"))

        # 追加処理
        name = request.form["name"]
        icon = request.files["icon"]
        filename = f"{name}.png"
        friends_dir = os.path.join(current_app.static_folder, "images", "friends")
        os.makedirs(friends_dir, exist_ok=True)
        icon.save(os.path.join(friends_dir, filename))

        db.session.add(Friend(user_id=user_id, name=name, icon_filename=filename))
        db.session.commit()
        return redirect(url_for("main.friends"))

    friends = Friend.query.filter_by(user_id=user_id).all()
    return render_template("friends.html", friends=friends)

@bp.route("/")
def index():
    # static/images/friends フォルダのPNGファイルを取得
    friends_dir = os.path.join(current_app.static_folder, "images", "friends")
    friend_files = [f for f in os.listdir(friends_dir) if f.lower().endswith(".png")]
    return render_template("index.html", friend_files=friend_files)
# @bp.route("/")
# def index():
#     user_id = session.get("user_id")
#     if not user_id:
#         return redirect(url_for("main.login"))

#     # DBからフレンド情報を取得
#     friends = Friend.query.filter_by(user_id=user_id).all()
#     return render_template("index.html", friends=friends)

@bp.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]
        confirm = request.form["confirm"]

        if password != confirm:
            flash("パスワードが一致しません")
            return redirect(url_for("main.register"))

        if User.query.filter_by(username=username).first():
            flash("このユーザー名は既に使われています")
            return redirect(url_for("main.register"))

        user = User(username=username)
        user.set_password(password)
        db.session.add(user)
        db.session.commit()
        flash("登録完了！ログインしてください")
        return redirect(url_for("main.login"))

    return render_template("register.html")
