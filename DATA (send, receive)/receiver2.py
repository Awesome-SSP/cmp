import socket
import time
import os
import magic  # For file type detection

CHUNK_SIZE = 1024 * 1024  # 1MB
timestamp = time.strftime("%Y%m%d_%H%M%S")
raw_filename = f"received_file"

# Temporary file to receive raw data
temp_path = raw_filename + ".tmp"

s = socket.socket()
s.bind(("", 5001))
s.listen(1)
print("[✓] Waiting for incoming file...")

conn, addr = s.accept()
print(f"[✓] Connected from {addr}")

with open(temp_path, 'wb') as f:
    while True:
        chunk = conn.recv(CHUNK_SIZE)
        if chunk == b'EOF!':
            break
        if not chunk:
            break
        f.write(chunk)
        conn.send(b'ACK!')

conn.close()
s.close()

# Detect file type
mime = magic.Magic(mime=True)
detected_type = mime.from_file(temp_path)
print(f"[✓] Detected MIME type: {detected_type}")

# Map MIME types to extensions
extension_map = {
    'text/plain': '.txt',
    'application/zip': '.zip',
    'application/pdf': '.pdf',
    'image/jpeg': '.jpg',
    'image/png': '.png',
    'video/mp4': '.mp4',
    'application/octet-stream': '.bin'
}

extension = extension_map.get(detected_type, '.dat')  # Default to .dat if unknown
final_path = raw_filename + extension
os.rename(temp_path, final_path)

print(f"[✓] File saved as: {final_path}")
