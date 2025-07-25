import socket
import time
import struct

CHUNK_SIZE = 10 * 1024 * 1024
timestamp = time.strftime("%Y%m%d_%H%M%S")

def recv_all(sock, n):
    """Receive exactly n bytes"""
    data = b''
    while len(data) < n:
        packet = sock.recv(n - len(data))
        if not packet:
            return None
        data += packet
    return data

s = socket.socket()
s.bind(("", 5002))
s.listen(1)
print("[✓] Waiting for file...")

conn, addr = s.accept()
print(f"[✓] Connected to {addr}")

# Step 1: Receive extension
ext = conn.recv(10).decode().strip()
filename = f"received_file_{timestamp}{ext}"
print(f"[✓] Saving as: {filename}")

with open(filename, 'wb') as f:
    while True:
        # Step 2: Receive chunk size (4 bytes)
        chunk_size_data = recv_all(conn, 4)
        if not chunk_size_data:
            break
        
        chunk_size = struct.unpack("!I", chunk_size_data)[0]
        
        if chunk_size == 0:
            break  # End of file

        # Step 3: Receive actual chunk
        chunk = recv_all(conn, chunk_size)
        f.write(chunk)
        conn.send(b'ACK!')

conn.close()
s.close()
print(f"[✓] File saved successfully: {filename}")
