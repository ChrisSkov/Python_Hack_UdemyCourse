import portscanner

targets_ip = input('[+] * Enter target to scan for vulnerable open ports: ')
port_number = int(input('[+] * Enter number of ports to Scan(entering 100 will scan port 1-99): '))
vul_file = input('[+] * Enter path to file with vulnerable softwares: ')
print('\n')

portscanner.scan(targets_ip)
