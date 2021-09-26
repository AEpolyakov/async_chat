from socket import *
import time
import json
import sys
from log.client_log_config import client_logger, log
from threading import Thread


@log
def socket_init():
    client_socket = socket(AF_INET, SOCK_STREAM)
    client_logger.info('init ok')
    return client_socket


def make_json_byte_message(mes_from: str, mes_to=None, message=None):
    result = {
        "action": "presence",
        "time": time.time(),
        "from": {
            "account_name": mes_from,
        },
    }
    if message:
        result["action"] = "msg"
        result["to"] = mes_to
        result["encoding"] = "unicode_escape"
        result["message"] = message

    return json.dumps(result).encode('unicode_escape')


def client_send(sock, message):
    sock.send(message)
    return client_receive(sock)


def client_receive(sock):
    try:
        raw = sock.recv(1024).decode('unicode_escape')
        return json.loads(raw)
    except Exception:
        pass


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


def listener(sock):
    while True:
        response = client_receive(sock)
        if response:
            print(f"\n{response['from']['account_name']} says: {response['message']}\nyour message:", end='')


def user_interface(sock):
    login = input('your login:')
    while True:
        message = input('your message:')
        if message:
            json_package = make_json_byte_message(mes_from=login, message=message)
            response = client_send(sock, json_package)
            # print(parse_response(response))


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
