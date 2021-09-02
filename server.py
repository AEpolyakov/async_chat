from socket import *
import time


class Server:
    def __init__(self):
        self.addr = 'localhost'
        self.port = 7777
        self.socket = socket(AF_INET, SOCK_STREAM)
        self.socket.bind((self.addr, self.port))
        self.socket.listen(5)

    def accept(self):
        while True:
            client, client_address = self.socket.accept()
            print(f'{client=} {client_address=}')
            timestr = time.ctime(time.time()) + '\n'
            client.send(timestr.encode('utf-8'))
            client.close()


if __name__ == '__main__':
    server = Server()
    server.accept()
