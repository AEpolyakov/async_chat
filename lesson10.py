from client import Client
import dis
import re


class ClientClassVerifier:
    def __init__(self, client_class):
        self.examined_class = client_class
        with open('client_dis.txt', 'w') as f:
            dis.dis(Client, file=f)

        forbidden = ['accept', 'listen']
        must_be = ['socket', 'AF_INET', 'SOCK_STREAM']
        with open('client_dis.txt', 'r') as f:
            disasm = f.read()
            for string in forbidden:
                result = re.findall(rf"LOAD_METHOD.*\({string}\)", disasm)
                if result:
                    raise AttributeError(f"class {self.examined_class} should not have {string}: {result}")

            for string in must_be:
                result = re.findall(rf"LOAD_GLOBAL.*\({string}\)", disasm)
                if not result:
                    raise AttributeError(f"class {self.examined_class} should have {string}")


        print(f'class {self.examined_class} is valid')


if __name__ == "__main__":
    verifier = ClientClassVerifier(Client)
