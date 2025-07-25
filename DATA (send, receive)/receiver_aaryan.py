import socket
import ssl
import os
import zlib
import hashlib
from tqdm import tqdm
import logging

# === CONFIG ===
CHUNK_SIZE = 1024 * 1024
SAVE_DIR = "received_files"
os.makedirs(SAVE_DIR, exist_ok=True)
AUTH_TOKEN = "supersecuretoken"
CERTFILE = "cert.pem"
KEYFILE = "key.pem"

# === LOGGING ===
logging.basicConfig(filename='receiver.log', level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# === HELPERS ===
def calculate_sha256(filepath):
    sha = hashlib.sha256()
    with open(filepath, 'rb') as f:
        while chunk := f.read(CHUNK_SIZE):
            sha.update(chunk)
    return sha.hexdigest()

# === SOCKET SETUP ===
context = ssl.SSLContext(ssl.PROTOCOL_TLS_SERVER)
context.load_cert_chain(certfile=CERTFILE, keyfile=KEYFILE)

server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.bind(('0.0.0.0', 5001))
server_socket.listen(1)
print("📡 Server listening securely on port 5001...")

while True:
    client, addr = server_socket.accept()
    with context.wrap_socket(client, server_side=True) as ssock:
        logging.info(f"Connected from {addr}")
        try:
            # === AUTH ===
            token = ssock.recv(64).decode()
            if token != AUTH_TOKEN:
                ssock.sendall(b'NOPE')
                continue
            ssock.sendall(b'OKAY')

            # === METADATA ===
            metadata = ssock.recv(2048).decode()
            filename, filesize, expected_hash = metadata.split("|")
            filename = os.path.basename(filename)
            filepath = os.path.join(SAVE_DIR, f"received_{filename}")
            filesize = int(filesize)

            ssock.sendall(b'RDY!')

            # === RESUME SUPPORT ===
            offset = os.path.getsize(filepath) if os.path.exists(filepath) else 0
            ssock.recv(4)  # Wait for REQO
            ssock.sendall(str(offset).zfill(32).encode())

            with open(filepath, 'ab') as f, tqdm(total=filesize, initial=offset, unit='B', unit_scale=True, desc='Downloading') as pbar:
                while True:
                    header = ssock.recv(4)
                    if header == b'EOF!':
                        break
                    chunk_len = int.from_bytes(header, 'big')
                    chunk = ssock.recv(chunk_len)
                    decompressed = zlib.decompress(chunk)
                    f.write(decompressed)
                    ssock.sendall(b'ACK!')
                    pbar.update(len(decompressed))

            # === VERIFY ===
            received_hash = calculate_sha256(filepath)
            if received_hash == expected_hash:
                print("✅ File received and verified.")
            else:
                print("❌ Hash mismatch!")
                logging.error(f"Expected: {expected_hash}, Got: {received_hash}")

        except Exception as e:
            logging.error(f"Error: {e}")
            ssock.close()