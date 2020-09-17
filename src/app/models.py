# Based on code from Faraz, gitlab.com/secdim/lectures/secure-programming/lab-vm.git

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
    dob = db.Column(db.DateTime)
    postcode = db.Column(db.Integer)
    __searchable__ = ["username"]

    def set_password(self, password):
        self.password = password

    def check_password(self, password):
        return self.password == password

    def __repr__(self):
        return "<User {}>".format(self.username)
