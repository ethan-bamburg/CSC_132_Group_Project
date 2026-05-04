"""
This file will be used to launch the app
"""
from flask import Flask, render_template, url_for, jsonify, request
from flask_sqlalchemy import SQLAlchemy
# from flask_socketio import SocketIO
from datetime import datetime
import threading
import time

print("🔥 RUNNING THIS FILE")

app = Flask(__name__)
#socketio = SocketIO(app)
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

"""
@app.route('/trigger')
def trigger_js():
    socketio.emit('run_js', {'msg': 'hello from python'})
    return {'status': 'ok'}
"""
def background_worker():
    while True:
        print("Running in background...")
        
        time.sleep(5)

@app.route('/run-task', methods=['POST'])
def run_task():
    data = request.get_json()
    task = data['task']

     # Simulated Python logic
    if task == "task1":
        result = "Dashboard task completed"
    elif task == "task2":
        result = "Data viewer processed data"
    elif task == "task3":
        result = "Settings updated"
    else:
        result = "Unknown task"

    return jsonify({"result": result})


@app.route('/')
def index():
    print("HOME ROUTE HIT")
    return render_template('index.html')

# threading.Thread(target=background_worker, daemon=True).start()

if __name__ == "__main__":
    print("🔥 HOME ROUTE HIT")
    app.run(debug=True)
    
   # socketio.run(app, debug=True)