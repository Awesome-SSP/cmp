import magic
import os
import time

# Create a temp file for simulation (normally you'd receive this)
with open(r"C:\Users\GAURAV\Desktop\cmp-main\received_file.tmp", "wb") as f:
    f.write(open("your_input_file.ext", "rb").read())  # use any file here

# Detect file type
mime = magic.Magic(mime=True)
mime_type = mime.from_file("received_file.tmp")
print("MIME Type Detected:", mime_type)

# Map MIME types to extensions
extension_map = {
    "text/plain": ".txt",
    "application/pdf": ".pdf",
    "application/zip": ".zip",
    "image/jpeg": ".jpg",
    "image/png": ".png",
    "image/gif": ".gif",
    "video/mp4": ".mp4",
    "application/octet-stream": ".bin"
}

# Get extension or default to .dat
extension = extension_map.get(mime_type, ".dat")
timestamp = time.strftime("%Y%m%d_%H%M%S")
final_name = f"received_file_{timestamp}{extension}"

# Rename the temp file
os.rename("received_file.tmp", final_name)

print(f"[✓] File saved as: {final_name}")
