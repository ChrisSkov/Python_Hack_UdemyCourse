import socket
from IPy import IP

port = 80


def check_ip(ip):
    try:
        IP(ip)
        return (ip)
    except ValueError:
        return socket.gethostbyname(ip)


def scan_port(ipaddress, port):
    try:
        sock = socket.socket()
        sock.settimeout(0.5)
        sock.connect((ipaddress, port))
        print('[+] Port' + str(port) + ' is open')
    except:
        print('[-] Port ' + str(port) + ' is closed')


ipaddress = input('[+] Enter scanning target: ')
converted_ip = check_ip(ipaddress)

for port in range(75, 85):
    scan_port(converted_ip, port)
