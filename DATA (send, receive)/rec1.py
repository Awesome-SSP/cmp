import socket

CHUNK_SIZE = 1024 * 1024
filename = "received_file.dat"

s = socket.socket()
s.bind(("", 5001))
s.listen(1)
conn, addr = s.accept()

with open(filename, 'wb') as f:
    while True:
        chunk = conn.recv(CHUNK_SIZE)
        if chunk == b'EOF!':
            break
        if not chunk:
            break
        f.write(chunk)
        conn.send(b'ACK!')  # Send acknowledgment

conn.close()
s.close()
print("File received.")