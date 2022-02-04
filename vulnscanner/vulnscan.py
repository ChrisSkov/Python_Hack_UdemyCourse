import portscanner

targets_ip = input('[+] * Enter target to scan for vulnerable open ports: ')
port_number = int(input('[+] * Enter number of ports to Scan(entering 100 will scan port 1-99): '))
vul_file = input('[+] * Enter path to file with vulnerable softwares: ')
print('\n')
target = portscanner.PortScan(targets_ip, port_number)

target.scan()

with open(vul_file, 'r') as file:
    count = 0
    for banner in target.banners:
        file.seek(0)
        for line in file.readlines():
            if line.strip() in banner:
                print('[!!] Vulnerable banner: ' + banner + 'on port: ' + str(target.open_ports[count]))
    count += 1
