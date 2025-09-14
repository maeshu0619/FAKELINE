from . import db
import datetime

class Feed(db.Model):
    __tablename__ = "feeds"
    id = db.Column(db.Integer, primary_key=True)
    date = db.Column(db.String, default=lambda: datetime.date.today().isoformat())
    dog = db.Column(db.String)
    time = db.Column(db.String)
    fed = db.Column(db.Boolean, default=False)

class Trash(db.Model):
    __tablename__ = "trash"
    id = db.Column(db.Integer, primary_key=True)
    date = db.Column(db.String, default=lambda: datetime.date.today().isoformat())
    taken = db.Column(db.Boolean, default=False)
