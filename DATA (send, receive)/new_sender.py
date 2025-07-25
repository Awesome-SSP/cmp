import socket
import os
import struct

CHUNK_SIZE = 10 * 1024 * 1024
FILE_TO_SEND = r"C:\Users\Saurabh\Desktop\sample.pdf"

s = socket.socket()
s.connect(('127.0.0.1', 5002))

# Step 1: Send extension (fixed width 10 bytes)
extension = os.path.splitext(FILE_TO_SEND)[1]
s.sendall(extension.ljust(10).encode())

# Step 2: Send file in chunks with size prefix
with open(FILE_TO_SEND, 'rb') as f:
    while True:
        chunk = f.read(CHUNK_SIZE)
        if not chunk:
            break
        s.sendall(struct.pack("!I", len(chunk)))  # 4 bytes chunk size
        s.sendall(chunk)
        s.recv(4)  # Wait for ACK

# Step 3: Send zero-length to mark EOF
s.sendall(struct.pack("!I", 0))

s.close()
print("✅ File sent successfully.")
