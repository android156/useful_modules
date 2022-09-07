# 2. Написать функцию host_range_ping() (возможности которой основаны на функции из примера 1) для перебора i
# p-адресов из заданного диапазона. Меняться должен только последний октет каждого адреса. По результатам проверки
# должно выводиться соответствующее сообщение.

import platform
import sys
from subprocess import Popen, PIPE
import ipaddress
import threading
from tabulate import tabulate


def check_availability(command, availabilities, host):
    process = Popen(command, stdout=PIPE, stderr=PIPE)
    availabilities[host] = not bool(process.wait())


def host_range_ping(host_list):
    threads = {}
    availabilities = {}
    result_dict = {
        'Доступные': [],
        'Недоступные': [],
    }
    param = "-n" if platform.system().lower() == 'windows' else "-c"
    for host in host_list:
        command = ["ping", param, "1", host]
        threads[host] = threading.Thread(target=check_availability, args=(command, availabilities, host), daemon=True)
        threads[host].start()
    for host in host_list:
        threads[host].join()
        if availabilities[host]:
            result_dict['Доступные'].append(host)
        else:
            result_dict['Недоступные'].append(host)
    return result_dict


try:
    my_ip = input('Введите ip адрес: ')
    my_ip = ipaddress.ip_address(my_ip)
except ValueError:
    print('Это не ip-адрес!')

try:
    ip_amount = input('Введите кол-во адресов для проверки: ')
    if not ip_amount.isalnum():
        raise TypeError
    ip_amount = int(ip_amount)
    if ip_amount > 256:
        raise ValueError
    if str(my_ip).split('.')[2] != str(my_ip + ip_amount).split('.')[2]:
        raise IndexError
except TypeError:
    print('Можно менять только последний октет, максимальное число хостов 256')
    sys.exit(1)
except ValueError:
    print('Можно менять только последний октет, максимальное число хостов 256')
    sys.exit(1)
except IndexError:
    IndexError('Можно менять только последний октет, для этого IP надо выбрать диапазон поменьше')
    sys.exit(1)

host_list = [str(my_ip + i) for i in range(ip_amount)]
print(tabulate(host_range_ping(host_list), headers='keys', tablefmt="grid"))
