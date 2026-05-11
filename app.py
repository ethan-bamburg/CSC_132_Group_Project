"""
This file will be used to launch the app
"""
from flask import Flask, render_template, url_for, jsonify, request
from flask_sqlalchemy import SQLAlchemy
from flask_socketio import SocketIO
from datetime import datetime
from communicator import *
import threading
import time


app = Flask(__name__)
# 3 slashes is a relative path, 4 is an absolute path
# we call sqlite since it's built into python and its all we need
# data.db is the name of the database
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///data.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

socketio = SocketIO(app)


# initialize the database using the information from the app

db = SQLAlchemy(app)


class myTest(db.Model):
    id = db.Column(db.Integer, primary_key=True)

    date_stamp = db.Column(
        db.DateTime, 
        default=datetime.utcnow
    )

    blame = db.Column(db.String(10), nullable=False)

    # nullable means we don't want this to be blank
    content = db.Column(db.String(200), nullable=False)

    action = db.Column(db.String(100), nullable=False)

    def __repr__(self):
        return 'Item <%r>' % self.id


# once SQLite database is finalized,
# open the terminal and type the following:
# python3
# from app import db
# db.create_all()

"""
@app.route('/trigger')
def trigger_js():
    socketio.emit('run_js', {'msg': 'hello from python'})
    return {'status': 'ok'}
"""

ser = None

def background_worker():
    with app.app_context():
        while True:
            print("Running in background...")
            socketio.emit('run_js', {
                'msg': 'Monitoring...'
            })
            
            time.sleep(5)

@app.route('/run-task', methods=['POST'])
def run_task():
    data = request.get_json()
    task = data['task']

     # Simulated Python logic
    if task == "task1":
        result = "Changed Fan Mode"
    elif task == "task2":
        result = "Event Logs N/I"
    elif task == "task3":
        result = "Settings"
    else:
        result = "Unknown task"

    return jsonify({"result": result})


@app.route('/')
def index():
    return render_template('index.html')

if __name__ == "__main__":
    threading.Thread(target=background_worker, daemon=True).start()

    socketio.run(app, debug=True)
    
   # socketio.run(app, debug=True)