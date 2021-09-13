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
    import argparse

    parser = argparse.ArgumentParser()
    parser.add_argument('address', type=str, default='', help="address to connect")
    parser.add_argument('port', nargs='?', type=int, default=7777, help="port to connect")
    result = parser.parse_args(args)

    return result.address, result.port


def main():
    args = sys.argv
    address, port = get_args(args[1:])
    print(f'{address=} {port=}')

    client_socket = socket_init()
    server_response = socket_connect(client_socket, address, port)
    print(f'{server_response=}')


if __name__ == '__main__':
    try:
        main()
    except Exception:
        print('failed to connect to server')
