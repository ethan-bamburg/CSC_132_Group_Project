"""
This file will be used to launch the app
"""
from flask import Flask, render_template, url_for
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

app = Flask(__name__)
# 3 slashes is a relative path, 4 is an absolute path
# we call sqlite since it's built into python and its all we need
# test.db is the name of the database
app.config['SQLALCHEMY_DATABASE_URL'] = 'sqlite:///test.db'

# initialize the database using the information from the app
"""
db = SQLAlchemy(app)


class myTest(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    # nullable means we don't want this to be blank
    content = db.Column(db.String(200), nullable=False)
    date_stamp = db.Column(db.DateTime, default=datetime.utcnow)

    def __rep__(self):
        return 'Item <%r>' % self.id
"""

# once SQLite database is finalized,
# open the terminal and type the following:
# python3
# from app import db
# db.create_all()

@app.route('/')
def index():
    return render_template('index.html')

if __name__ == "__main__":
    app.run(debug=True)