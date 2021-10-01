from client import Client
import dis


class ClientClassVerifier:
    def __init__(self, client_class):
        self.examined_class = client_class

    def check(self):
        print(dis.dis(self.examined_class))
        return


if __name__ == "__main__":
    client_class_verifier = ClientClassVerifier(Client)
    # client = Client(('address', 7777), 'login', 'to', 'mode')
    # client_verifier = ClientVerifier(client)

    print(client_class_verifier.check())
