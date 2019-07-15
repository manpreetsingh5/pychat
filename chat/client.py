import socket
import select
import errno

import sys

from flask import request

HEADER_LENGTH = 10
IP = "127.0.0.1"
PORT = 9311


class Client:

    def __init__(self, username):
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.username = username.encode('utf-8')
        self.username_header = "{:<{}}".format(len(username), HEADER_LENGTH).encode('utf-8')

        return


    def connect(self):
        self.socket.connect((IP, PORT))

        self.socket.setblocking(False)

    def listen(self):
        self.socket.listen()

    def message(self, message):

        self.socket.send(self.username_header + self.username)
        # while True:
            # message = input("{} > ".format(self.username.decode('utf-8')))
            # message = request.form['myMessage']
        print("MESSAGE IS: " + message)
        if message:
            message = message.encode('utf-8')
            message_header = "{:<{}}".format(len(message), HEADER_LENGTH).encode('utf-8')
            self.socket.send(message_header + message)

        try:
            while True:
                # Receive messages
                username_header = self.socket.recv(HEADER_LENGTH)
                if not len(username_header):
                    print("Connection closed by client")
                    sys.exit()

                username_length = int(username_header.decode('utf-8').strip())
                username = self.socket.recv(username_length).decode('utf-8')

                message_header = self.socket.recv(HEADER_LENGTH)
                message_length = int(message_header.decode('utf-8').strip())
                message = self.socket.recv(message_length).decode('utf-8')

                print("{}: {}".format(username, message))
        except IOError as e:
            if e.errno != errno.EAGAIN and e.errno != errno.EWOULDBLOCK:
                print("Reading error", str(e))
                sys.exit()

        except Exception as e:
            print('General Error', str(e))
            sys.exit()

    def receive_message(self, client):
        try:
            message_header = client.recv(HEADER_LENGTH)
            if not len(message_header):
                return False

            message_length = int(message_header.decode("utf-8").strip())
            return {"header":message_header,"data":client.recv(message_length)}

        except:
            return False


