print('\n#### задание 1 ####\n')
import subprocess
import ipaddress
import re
import tabulate


def host_ping(ip_list: list):
    for ip in ip_list:
        process = subprocess.Popen(['ping', '-c', '1', ip], stdout=subprocess.PIPE)
        string = process.stdout.read().decode('utf-8')
        try:
            result = re.findall(r'time=.*', string)[0]
            print(f'Узел "{ip}" доступен')
        except Exception:
            print(f'Узел "{ip}" НЕдоступен')


ip_list = ['127.0.0.1', '127.0.0.2', '192.168.142.4', '192.168.142.200']
host_ping(ip_list)


print('\n#### задание 2 ####\n')


def host_range_ping(ip: str, ip_range: int):
    ip_address = ipaddress.ip_address(ip)
    ip_list = [str(ip_address + i) for i in range(ip_range)]
    host_ping(ip_list)


host_range_ping('127.0.0.1', 5)

print('\n#### задание 3 ####\n')

def host_range_ping_tab(ip_start: str, ip_range: int):

    ip_address = ipaddress.ip_address(ip_start)

    result_dict = {"reachable": [],
                   "unreachable": []}

    for i in range(ip_range):
        ip = ip_address + i
        process = subprocess.Popen(['ping', '-c', '1', str(ip)], stdout=subprocess.PIPE)
        string = process.stdout.read().decode('utf-8')
        try:
            result = re.findall(r'time=' + r'.*', string)[0]
            result_dict["reachable"].append(ip)
        except Exception:
            result_dict["unreachable"].append(ip)
    print(tabulate.tabulate(result_dict, headers="keys"))


host_range_ping_tab('127.0.0.253', 5)

