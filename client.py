from socket import *
import time
import json
import sys


def socket_init():
    s = socket(AF_INET, SOCK_STREAM)
    return s


def socket_connect(s, address, port):
    s.connect((address, port))

    presence = make_json_byte_presence()
    s.send(presence)

    response = s.recv(1024)
    s.close()
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
        raise Exception('адрес не указан!!!')

    port = 7777
    try:
        port = int(args[2])
    except Exception:
        print('')

    return address, port


if __name__ == '__main__':
    args = sys.argv
    address, port = get_args(args)
    print(f'{address=} {port=}')

    client_socket = socket_init()
    server_response = socket_connect(client_socket, address, port)
    print(f'{server_response=}')
