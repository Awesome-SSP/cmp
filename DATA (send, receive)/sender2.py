import socket
import os

CHUNK_SIZE = 1024 * 1024  # 1MB
filename = "your_file_here.pdf"  # Replace with your file
file_ext = os.path.splitext(filename)[1]  # e.g., '.pdf'

server_ip = "DESTINATION_IP"
server_port = 5001

s = socket.socket()
s.connect((server_ip, server_port))

# Step 1: Send the extension first
s.send(file_ext.encode().ljust(10))  # pad to fixed size (10 bytes)

# Step 2: Send file content in chunks
with open(filename, 'rb') as f:
    chunk_num = 0
    while True:
        chunk = f.read(CHUNK_SIZE)
        if not chunk:
            break
        s.sendall(chunk)
        ack = s.recv(4)
        if ack != b'ACK!':
            print(f"[!] Chunk #{chunk_num} not acknowledged. Resending...")
            f.seek(chunk_num * CHUNK_SIZE)
            continue
        chunk_num += 1

# Step 3: Send EOF marker
s.send(b'EOF!')

s.close()
print("[✓] File sent.")
