import socket
import time
import os

CHUNK_SIZE = 10 * 1024 * 1024
timestamp = time.strftime("%Y%m%d_%H%M%S")

s = socket.socket()
s.bind(("", 5002))
s.listen(1)
print("[✓] Waiting for file...")

conn, addr = s.accept()
print(f"[✓] Connected to {addr}")

# Step 1: Receive file extension (fixed size, 10 bytes)
ext = conn.recv(10).decode().strip()
print(f"[✓] Extension received: {ext}")

# Step 2: Auto-generate final filename
filename = f"received_file_{timestamp}{ext}"
print(f"[✓] Saving as: {filename}")
count = 0
with open(filename, 'wb') as f:
    
    while True:
        print(count)
        chunk = conn.recv(CHUNK_SIZE)
        if chunk == b'EOF!':
            break
        if not chunk:
            break
        f.write(chunk)
        count +=1
        conn.send(b'ACK!')

conn.close()
s.close()
print(f"[✓] File saved successfully: {filename}")
