from queue import Queue

from flask import Flask, render_template, request
from threading import Thread

from multiprocessing import Process

from flask import make_response
from flask import session

from chat import server, client

app = Flask(__name__)
app.secret_key = 'SECRET'
# session = sessions.SecureCookieSession
SERVER = server.Server()
SERVER.bind()
SERVER.listen()
SERVER_THREAD = Thread(target=SERVER.channel)
SERVER_THREAD.setDaemon(True)
SERVER_THREAD.start()
# # SERVER_THREAD.join()

@app.route('/')
def hello_world():

    return render_template('login.html')


def client_thread(username):
    client2 = client.Client(username)
    client2.connect()
    SERVER.objs[username] = client2

@app.route('/handleLogin', methods=['POST'])
def handleLogin():
    username = request.form['username']
    # new_client = client.Client(username)
    CLIENT__INIT_THREAD = Thread(target=client_thread, args=[username])
    CLIENT__INIT_THREAD.setDaemon(True)
    CLIENT__INIT_THREAD.start()
    CLIENT__INIT_THREAD.join()

    # if CLIENT__INIT_THREAD.is_alive():
    #     CLIENT__INIT_THREAD.join()
    print(username)
    # new_client = que.get()
    # CLIENT_THREAD = Thread(target=new_client.message,args=[""], daemon=True)
    # CLIENT_THREAD.start()
    # session['Client'] = new_client
    resp = make_response(render_template('index.html', messages=SERVER.messages2))
    resp.set_cookie('user', username)
    return resp


@app.route('/handleClient', methods=['GET', 'POST'])
def handleClient():
    if request.method == 'GET':
        return {'data':SERVER.messages2}

    elif request.method == 'POST':
        message = request.form['myMessage']
        if message:
            SERVER.objs[request.cookies.get('user')].message(message)
        return render_template('index.html', messages={'data':SERVER.messages2})


# @app.route('/exit')
# def leave():
#     main.close()
