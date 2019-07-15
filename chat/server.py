import socket
import select

HEADER_LENGTH = 10
IP = "127.0.0.1"
PORT = 9311


class Server:

    def __init__(self):
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.sockets_list = [self.socket]
        self.clients = {}
        self.objs = {}
        self.messages2 = []
        return


    def bind(self):
        self.socket.bind((IP, PORT))
        print("Initialized Server")

    def listen(self):
        self.socket.listen()

    def addsocket(self, client):
        self.sockets_list.append(client)

    def receive_message(self, client):
        try:
            print("RECEIVED MESSAGE")
            message_header = client.recv(HEADER_LENGTH)
            if not len(message_header):
                return False

            print(message_header.decode('utf-8'))

            message_length = int(message_header.decode("utf-8").strip())
            return {"header":message_header,"data":client.recv(message_length)}

        except:
            print("nope")
            return False

    def channel(self):
        while True:
            read_sockets, _, error_sockets = select.select(self.sockets_list, [], self.sockets_list)
            print(read_sockets)

            for notified_socket in read_sockets:
                if notified_socket == self.socket:
                    client_socket, client_addr = self.socket.accept()


                    user = self.receive_message(client_socket)
                    if user == False:
                        continue

                    print("Accepted new connection from {} :{} username:{}".format(client_addr[0], client_addr[1], user['data'].decode('utf-8')))
                    self.addsocket(client_socket)
                    self.clients[client_socket] = user



                else:
                    message = self.receive_message(notified_socket)

                    if message == False:
                        print("Closed connections from {}".format(self.clients[notified_socket]['data'].decode('utf-8')))
                        self.sockets_list.remove(notified_socket)
                        del self.clients[notified_socket]
                        continue

                    user = self.clients[notified_socket]
                    print("Received message from {}:{}".format(user['data'].decode('utf-8'), message['data'].decode('utf-8')))
                    username = user['data'].decode('utf-8')
                    message2 = message['data'].decode('utf-8')
                    print('USERNAME: ', username)
                    print('MESSAGE: ', message2)
                    self.messages2.append({'user':username, 'message':message2})
                    print(self.messages2)
                    for client in self.clients:
                        if client != notified_socket:
                            client.send(user['header'] + user['data'] + message['header'] + message['data'])

            for error_socket in error_sockets:
                self.sockets_list.remove(error_socket)
                del self.clients[error_socket]

    def close(self):
        self.socket.close()
