import socket

CHUNK_SIZE = 1024 * 1024
filename = "received_file.dat"

s = socket.socket()
s.bind(("", 5001))
s.listen(1)
conn, addr = s.accept()
count = 0
with open(filename, 'wb') as f:
    
    while True:
        count +=1
        print(count)
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