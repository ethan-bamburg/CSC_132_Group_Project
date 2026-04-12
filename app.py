"""
This file will be used to launch the app
"""
from flask import Flask
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

# SQLite database goes here

@app.route('/')
def index():
    return "Webpage test"

if __name__ == "__main__":
    app.run(debug=True)