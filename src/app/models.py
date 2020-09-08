from app import db, login
from datetime import datetime
from flask_login import UserMixin
from sqlalchemy.sql import text
from sqlalchemy.exc import OperationalError

@login.user_loader
def load_user(id):
    return User.query.get(int(id))

class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), index=True, unique=True)
    email = db.Column(db.String(120), index=True, unique=True)
    password = db.Column(db.String(64))
    posts = db.relationship("Post", backref="author", lazy="dynamic")
    __searchable__ = ["username"]

    def set_password(self, password):
        self.password = password

    def check_password(self, password):
        return self.password == password

    def __repr__(self):
        return "<User {}>".format(self.username)

class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    body = db.Column(db.String(140))
    timestamp = db.Column(db.DateTime, index=True, default=datetime.utcnow)
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"))
    __searchable__ = ["body"]

    def all_posts():
        return Post.query.all()

    def filter_posts(search_term):
        return db.session.query(Post).filter(text("body LIKE '%%{}%%'".format(search_term))).all()

    def __repr__(self):
        return "<Post {}>".format(self.body)
