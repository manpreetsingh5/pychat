from queue import Queue

from flask import Flask, render_template, request
import os

from flask_socketio import SocketIO, join_room, emit

app = Flask(__name__)
app.secret_key = 'SECRET'
socketio = SocketIO(app)
ROOMS = {}

@app.route('/')
def index(methods=['GET', 'POST']):
    print(os.getcwd())
    return render_template('index.html')

def messageReceived(methods=['GET', 'POST']):
    print('message was received!!!')

@socketio.on('my event')
def handle_my_custom_event(json, methods=['GET', 'POST']):
    print('received my event: ' + str(json))
    socketio.emit('my response', json, callback=messageReceived)

if __name__ == '__main__':
    socketio.run(app, debug=True)
