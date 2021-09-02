from socket import *
import time
import json
import sys


class Client:
    def __init__(self, args):
        self.port = self.get_port(self, args)
        self.address = self.get_addr(self, args)
        self.socket = socket(AF_INET, SOCK_STREAM)
        print(f'{self.port=} {self.address=}')

    def connect(self):
        self.socket.connect((self.address, self.port))
        presence = self.make_json_byte_presence()

        print(f'{presence=}')

        self.socket.close()
        return

    @staticmethod
    def make_json_byte_presence():
        presence = {
            "action": "presence",
            "time": time.time(),
            "type": "status",
            "user": {
                "account_name": "test_user",
                "status": "online",
            }
        }
        return json.dumps(presence).encode('utf-8')

    @staticmethod
    def get_addr(self, args):
        addr = 'localhost'
        if len(sys.argv) > 1:
            for i in range(len(args)):
                try:
                    if args[i] == '-a':
                        addr = str(args[i + 1])
                except Exception:
                    print('failed to change addr. Port is set to "localhost"')
        return addr

    @staticmethod
    def get_port(self, args):
        port = 7777
        if len(sys.argv) > 1:
            for i in range(len(args)):
                try:
                    if args[i] == '-p':
                        port = int(args[i+1])
                except Exception:
                    print('failed to change port. Port is set to 7777')
        return port


if __name__ == '__main__':
    client = Client(sys.argv)
    client.connect()
