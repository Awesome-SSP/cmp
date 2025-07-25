import socket
import os

CHUNK_SIZE = 1024 * 1024  # 1MB
filename = "heavy_file.dat"
server_ip = "192.168.1.22"
server_port = 5001

s = socket.socket()
s.connect((server_ip, server_port))

with open(filename, 'rb') as f:
    chunk_num = 0
    while True:
        chunk = f.read(CHUNK_SIZE)
        if not chunk:
            break
        s.sendall(chunk)
        ack = s.recv(4)
        if ack != b'ACK!':
            print(f"Retransmitting chunk #{chunk_num}")
            f.seek(chunk_num * CHUNK_SIZE)
            continue
        chunk_num += 1

s.send(b'EOF!')
s.close()
print("File sent.")
