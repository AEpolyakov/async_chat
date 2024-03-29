from socket import *
import time
import sys
import json


def socket_init(address, port):
    s = socket(AF_INET, SOCK_STREAM)
    s.bind((address, port))
    s.listen(5)
    return s


def get_answer(action=None):
    if action == 'presence':
        return {
            "response": 200,
            "alert": "Необязательное сообщение/уведомление",
        }
    return {
            "response": 400,
            "alert": "bad request",
        }


def decode_message(raw):
    try:
        client_message = raw.decode('unicode_escape')
        return json.loads(client_message)
    except Exception:
        print('failed to decode message')
    return None


def server_accept(s):
    while True:
        client, client_address = s.accept()
        client_message = decode_message(client.recv(1024))
        answer = get_answer(client_message['action'])
        print(f'{client_message=}\n{answer=}')
        client.send(json.dumps(answer).encode('utf-8'))
        client.close()


def get_args(args):
    import argparse

    parser = argparse.ArgumentParser()
    parser.add_argument('-a', type=str, default='', help="socket address")
    parser.add_argument('-p', type=int, default=7777, help="socket port")
    result = parser.parse_args(args)

    return result.a, result.p


def main():
    socket_address, socket_port = get_args(sys.argv[1:])
    print(f'{socket_address=} {socket_port=}')

    server_socket = socket_init(socket_address, socket_port)
    server_accept(server_socket)


if __name__ == '__main__':
    try:
        main()
    except Exception:
        print('failed to start server')
