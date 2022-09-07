# 1. Написать функцию host_ping(), в которой с помощью утилиты ping будет проверяться
# доступность сетевых узлов. Аргументом функции является список, в котором каждый сетевой
# узел должен быть представлен именем хоста или ip-адресом. В функции необходимо
# перебирать ip-адреса и проверять их доступность с выводом соответствующего сообщения
# («Узел доступен», «Узел недоступен»). При этом ip-адрес сетевого узла должен создаваться с
# помощью функции ip_address().


import platform
from subprocess import Popen, PIPE
import chardet
import ipaddress
import socket
import threading
from tabulate import tabulate


def decrypt_data(encrypted_data):
    encoding = chardet.detect(encrypted_data).get('encoding')
    if encoding:
        decrypted_data = encrypted_data.decode(encoding)
    else:
        decrypted_data = encrypted_data.decode()
    return decrypted_data


def check_availability(command, availabilities, index):
    process = Popen(command, stdout=PIPE, stderr=PIPE)
    availabilities[index] = not bool(process.wait())


def host_ping(host_list):
    threads = {}
    availabilities = {}
    result_table = [('Имя хоста', 'ip адрес', 'Доступность')]
    param = "-n" if platform.system().lower() == 'windows' else "-c"
    for i, host in enumerate(host_list):
        command = ["ping", param, "2", host]
        threads[i] = threading.Thread(target=check_availability, args=(command, availabilities, i), daemon=True)
        threads[i].start()
        print(f'Поток {i+1} запущен.')
    for i, host in enumerate(host_list):
        host_name = host
        try:
            host_ip = ipaddress.ip_address(socket.gethostbyname(host))
        except socket.gaierror:
            host_ip = 'Отсутствует'
        threads[i].join()
        print(f'Поток {i + 1} завершен.')
        result_table.append((host_name, host_ip, availabilities[i]))
    return result_table


host_list = ['yandex.ru', 'google.com', '8.8.8.8', 'instagram.com', 'aaa', 123]
host_list = [str(el) for el in host_list]
print(tabulate(host_ping(host_list), headers='firstrow'))

