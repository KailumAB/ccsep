# Based on code from Faraz, gitlab.com/secdim/lectures/secure-programming/lab-vm.git

from app import app, db
from app.models import User
from sqlalchemy.sql import text

@app.shell_context_processor
def make_shell_context():
    return {"db": db, "User": User, "text": text}
