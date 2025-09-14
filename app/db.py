import sqlite3
import datetime
from flask import current_app

DOGS = ["てつ", "ぽんず"]
TIMES = ["朝", "昼", "夜"]

def _connect():
    return sqlite3.connect(current_app.config["DB_PATH"])

def init_db_for_today():
    """本日のレコード（てつ/ぽんず × 朝/昼/夜 = 6件）がなければ作成"""
    today = datetime.date.today().isoformat()
    with _connect() as con:
        cur = con.cursor()
        cur.execute("""
            CREATE TABLE IF NOT EXISTS feeds (
                id   INTEGER PRIMARY KEY AUTOINCREMENT,
                date TEXT,
                dog  TEXT,
                time TEXT,
                fed  INTEGER
            )
        """)
        for dog in DOGS:
            for t in TIMES:
                cur.execute(
                    "SELECT 1 FROM feeds WHERE date=? AND dog=? AND time=?",
                    (today, dog, t)
                )
                if cur.fetchone() is None:
                    cur.execute(
                        "INSERT INTO feeds(date, dog, time, fed) VALUES (?,?,?,0)",
                        (today, dog, t)
                    )
        con.commit()

def get_state_for_today():
    """本日の給餌状況を辞書 {(dog, time): fed} で返す"""
    today = datetime.date.today().isoformat()
    with _connect() as con:
        cur = con.cursor()
        cur.execute(
            "SELECT dog, time, fed FROM feeds WHERE date=? ORDER BY dog, time",
            (today,)
        )
        rows = cur.fetchall()
    return {(dog, t): fed for dog, t, fed in rows}, today

def toggle_feed_today(dog, t):
    """本日の dog/t の fed をトグル"""
    today = datetime.date.today().isoformat()
    with _connect() as con:
        cur = con.cursor()
        cur.execute(
            "SELECT fed FROM feeds WHERE date=? AND dog=? AND time=?",
            (today, dog, t)
        )
        row = cur.fetchone()
        if row is None:
            # 無ければ安全側で0作成→1にする
            cur.execute(
                "INSERT INTO feeds(date, dog, time, fed) VALUES (?,?,?,0)",
                (today, dog, t)
            )
            fed = 0
        else:
            fed = row[0]
        newval = 0 if fed else 1
        cur.execute(
            "UPDATE feeds SET fed=? WHERE date=? AND dog=? AND time=?",
            (newval, today, dog, t)
        )
        con.commit()

def init_trash_for_today():
    today = datetime.date.today().isoformat()
    with _connect() as con:
        cur = con.cursor()
        cur.execute("""
            CREATE TABLE IF NOT EXISTS trash (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                date TEXT,
                taken INTEGER
            )
        """)
        cur.execute("SELECT * FROM trash WHERE date=?", (today,))
        if cur.fetchone() is None:
            cur.execute("INSERT INTO trash(date, taken) VALUES (?,0)", (today,))
        con.commit()

def get_trash_for_today():
    today = datetime.date.today().isoformat()
    with _connect() as con:
        cur = con.cursor()
        cur.execute("SELECT taken FROM trash WHERE date=?", (today,))
        row = cur.fetchone()
    return (row[0] if row else 0)

def toggle_trash_today():
    today = datetime.date.today().isoformat()
    with _connect() as con:
        cur = con.cursor()
        cur.execute("SELECT taken FROM trash WHERE date=?", (today,))
        taken = cur.fetchone()[0]
        newval = 0 if taken else 1
        cur.execute("UPDATE trash SET taken=? WHERE date=?", (newval, today))
        con.commit()
