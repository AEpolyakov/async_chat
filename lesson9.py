# задание 1
import subprocess
import ipaddress
import socket
import re
import tabulate


def host_ping(host_list: list, printable=True):
    result_dict = {"reachable": [],
                   "unreachable": []}

    for host in host_list:
        try:
            ip_address = ipaddress.ip_address(host)
        except:
            try:
                ip_address = ipaddress.ip_address(socket.gethostbyname(host))
            except:
                ip_address = ''

        process = subprocess.Popen(['ping', '-c', '1', str(ip_address)], stdout=subprocess.PIPE)
        string = process.stdout.read().decode('utf-8')
        try:
            result = re.findall(r'time=.*', string)[0]
        except Exception:
            result_dict["unreachable"].append(host)
            if printable:
                print(f'Узел "{host}" НЕдоступен')
        else:
            result_dict["reachable"].append(host)
            if printable:
                print(f'Узел "{host}" доступен')

    return result_dict


host_list = ['127.0.0.1', '127.0.0.2', 'google.com', '192.168.142.200']
host_ping(host_list)


# задание 2


def host_range_ping(ip_range: str, printable=True):
    try:
        ip_network = ipaddress.ip_network(ip_range)
    except Exception as ex:
        print(f'bad ip range {ex}')
    else:
        ip_list = [ip_address for ip_address in ip_network]
        return host_ping(host_list=ip_list, printable=printable)


host_range_ping('127.0.0.0/27')

# задание 3


def host_range_ping_tab(ip_range: str):
    result_dict = host_range_ping(ip_range, printable=False)
    print(tabulate.tabulate(result_dict, headers="keys"))


host_range_ping_tab('127.0.0.0/27')


# задание 4

def start_clients(client_list: list):
    for client in client_list:
        process = subprocess.Popen([f'python {client}'],
                                   stdout=subprocess.PIPE,
                                   stdin=subprocess.PIPE,
                                   stderr=subprocess.PIPE,
                                   shell=True)
        string = process.communicate(input=b'exit')
        print(f'{string=}\n')


port = 7777
client_list = [f'client.py -l user4 -p {port}', f'client.py -l user5 -t user1 -p {port}']
start_clients(client_list)
