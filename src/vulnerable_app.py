# Based on code from Faraz, Vulnerable App

from app import app, db
from app.models import User
from sqlalchemy.sql import text

@app.shell_context_processor
def make_shell_context():
    return {"db": db, "User": User, "text": text}
