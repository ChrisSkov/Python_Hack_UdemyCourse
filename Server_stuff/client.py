import socket

HOST = "10.77.77.26"
PORT = 65432

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.connect((HOST, PORT))
    hostname = socket.gethostname()
    to_send = hostname.encode()
    s.send(to_send)
    data = s.recv(1024)

print(f"Recieved {data!r}")