from socket import *
import time
import json
import sys
from log.client_log_config import client_logger, log
from threading import Thread
import argparse


@log
def socket_init():
    client_socket = socket(AF_INET, SOCK_STREAM)
    client_logger.info('init ok')
    return client_socket


def make_message(mes_from: str, mes_to=None, message=None):
    result = {
        "action": "msg",
        "time": time.time(),
        "from": {
            "account_name": mes_from,
        },
        "mess_to": mes_to,
        "message": message,
        "encoding": "unicode_escape",
    }
    return make_json(result)


def make_presence(mes_from: str):
    result = {
        "action": "presence",
        "time": time.time(),
        "from": {
            "account_name": mes_from,
        },
    }
    return make_json(result)


def make_json(string: dict):
    return json.dumps(string).encode('unicode_escape')


def client_send(sock, message):
    sock.send(message)
    return client_receive(sock)


def client_receive(sock):
    try:
        raw = sock.recv(1024).decode('unicode_escape')
        return json.loads(raw)
    except Exception:
        pass


def get_args(args):
    parser = argparse.ArgumentParser()
    parser.add_argument('address', nargs='?', type=str, default='', help="address to connect")
    parser.add_argument('port', nargs='?', type=int, default=7777, help="port to connect")
    result = parser.parse_args(args)

    return result.address, result.port


def listener(sock):
    while True:
        response = client_receive(sock)
        try:
            print(f"\n{response['from']['account_name']} says: {response['message']}\n>>", end='')
        except Exception:
            pass


def user_interface(sock):
    login = input('your login:')
    presence = make_presence(login)
    # client_send(sock, presence)

    message_to = input('message to (empty to everyone):')
    while True:
        message = input('>>')
        if message:
            json_package = make_message(mes_from=login, mes_to=message_to, message=message)
            response = client_send(sock, json_package)


def parse_response(response):
    return f"\n{response['from']} says: {response['message']}"


def main():
    address, port = get_args(sys.argv[1:])

    client_socket = socket_init()
    client_socket.connect((address, port))

    t1 = Thread(target=listener, args=(client_socket, ))
    t2 = Thread(target=user_interface, args=(client_socket, ))
    t1.start()
    t2.start()


if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        print('stopped by user')
    except Exception:
        client_logger.critical(f'failed to connect to server')
