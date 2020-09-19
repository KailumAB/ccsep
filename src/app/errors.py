# Based on code from Faraz, gitlab.com/secdim/lectures/secure-programming/lab-vm.git

from flask import render_template
from app import app, db

@app.errorhandler(404)
def not_found_error(error):
    return render_template("404.html"), 404
