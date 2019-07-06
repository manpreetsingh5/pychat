from flask import Flask, render_template

from chat import server

app = Flask(__name__)

main = server.Server()
main.bind()
# main.listen()
# main.channel()

@app.route('/')
def hello_world():

    return render_template('index.html')


def login():
    return render_template('login.html')

# @app.route('/exit')
# def leave():
#     main.close()
