from socket import *
import time
import sys
import json
from log.server_log_config import server_logger, log
import select


# class Clients:
#     def __init__(self):
#         self.clients = []
#
#     def append(self, connect):
#         self.clients.append({
#             "connect": connect,
#             "name": '',
#         })


class Server:
    def __init__(self, address):
        self.socket = self.non_blocking_socket(address)
        self.clients = []
        self.connections = []

    def start(self):
        while True:
            try:
                connection, address = self.socket.accept()
            except OSError as e:
                pass
            else:
                print("Получен запрос на соединение с %s" % str(address))
                self.clients.append({
                    "connection": connection,
                    "name": "",
                })
            finally:
                wait = 10
                w, r = [], []
                connections = self.get_connections()
                try:
                    r, w, e = select.select(connections, connections, [], wait)
                except Exception as ex:
                    pass

                requests = self.read_requests(r, self.connections)
                if requests:
                    self.write_responses(requests, w, self.connections)

    def get_connections(self):
        return [client["connection"] for client in self.clients]

    @staticmethod
    def get_answer(action=None):
        if action == 'presence':
            return {
                "response": 200,
                "alert": "ok",
            }
        return {
                "response": 400,
                "alert": "bad request",
            }

    @staticmethod
    def decode_message(raw):
        try:
            client_message = raw.decode('unicode_escape')
            return json.loads(client_message)
        except Exception:
            server_logger.error(f'failed to decode message: {raw}')
        return None

    @staticmethod
    def non_blocking_socket(address):
        sock = socket(AF_INET, SOCK_STREAM)
        sock.bind(address)
        sock.listen(5)
        sock.settimeout(0.2)
        return sock

    def analyse_response(self, responses: dict):
        try:
            for key in responses:
                if responses[key]["action"] == "presence":
                    print(f'{responses[key]["from"]}')
        except Exception:
            pass

    def read_requests(self, clients, all_clients):
        responses = {}

        for sock in clients:
            try:
                data = sock.recv(1024).decode('unicode_escape')
                responses[sock] = data
                self.analyse_response(responses)
            except Exception as ex:
                print(f'Клиент {sock.fileno()} {sock.getpeername()} отключился')
                all_clients.remove(sock)
        return responses

    @staticmethod
    def write_responses(requests, clients, all_clients):

        for sock in clients:
            try:
                for request in requests.values():
                    response = request.encode('unicode_escape')
                    sock.send(response)
            except Exception as ex:
                print(f'Клиент {sock.fileno()} {sock.getpeername()} отключился')
                sock.close()
                all_clients.remove(sock)


def get_args(args):
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument('-a', type=str, default='', help="socket address")
    parser.add_argument('-p', type=int, default=7777, help="socket port")
    result = parser.parse_args(args)
    return result.a, result.p


def main():
    socket_address = get_args(sys.argv[1:])

    server = Server(socket_address)
    server.start()


if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        server_logger.info('stopped by user')
    except Exception as ex:
        server_logger.critical(f'failed to start server, {ex}')