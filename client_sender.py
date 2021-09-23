from socket import *
from select import select
import sys

ADDRESS = ('localhost', 7777)


def echo_client():
    with socket(AF_INET, SOCK_STREAM) as sock:  # Создать сокет TCP
        sock.connect(ADDRESS)  # Соединиться с сервером
        while True:
            msg = input('Ваше сообщение: ')
            if msg == 'exit':
                break
            elif msg:
                sock.send(msg.encode('unicode_escape'))  # Отправить!


if __name__ == '__main__':
    echo_client()
