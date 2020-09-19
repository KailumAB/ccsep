#!/usr/bin/env python3

# Based on code from Faraz, gitlab.com/secdim/lectures/secure-programming/lab-vm.git

from flask import Flask
app = Flask(__name__)

@app.route('/')
def hello_world():
    return "Hello, world!"

if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=8000)
