import socket

HOST = "10.77.77.26"
PORT = 65432

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.bind((HOST, PORT))
    s.listen()
    conn, addr = s.accept()
    with conn:
        print(f"connected by {addr}")
        while True:
            data = conn.recv(1024)
            if not data:
                break
            conn.sendall(data)
            print('OS and username: ' + data.decode() + '\nIP Address:  ' + addr[0] + '\nPort:  ' + str(addr[1]))
