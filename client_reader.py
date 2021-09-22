from socket import *
from select import select
import sys

ADDRESS = ('localhost', 7777)


def echo_client():
    # Начиная с Python 3.2 сокеты имеют протокол менеджера контекста
    # При выходе из оператора with сокет будет автоматически закрыт
    with socket(AF_INET, SOCK_STREAM) as sock:  # Создать сокет TCP
        sock.connect(ADDRESS)  # Соединиться с сервером
        while True:
            data = sock.recv(1024).decode('unicode_escape')
            if data:
                print('Ответ:', data)


if __name__ == '__main__':
    echo_client()
