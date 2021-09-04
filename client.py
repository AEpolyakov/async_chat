from socket import *
import time
import json
import sys


def socket_init():
    client_socket = socket(AF_INET, SOCK_STREAM)
    return client_socket


def socket_connect(client_socket, address, port):
    client_socket.connect((address, port))

    presence = make_json_byte_presence()
    client_socket.send(presence)

    response = client_socket.recv(1024)
    client_socket.close()
    return response.decode('unicode_escape')


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
    return json.dumps(presence).encode('unicode_escape')


def get_args(args):
    address = ''
    try:
        address = str(args[1])
    except Exception:
        print('No address value. Address set to "localhost"')

    port = 7777
    try:
        port = int(args[2])
    except Exception:
        print('No port value. Port set to 7777')

    return address, port


def main():
    args = sys.argv
    address, port = get_args(args)
    print(f'{address=} {port=}')

    client_socket = socket_init()
    server_response = socket_connect(client_socket, address, port)
    print(f'{server_response=}')


if __name__ == '__main__':
    main()
