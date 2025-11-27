import socket
import os
import time

HOST = '127.0.0.1'
PORT = 65432
FILE_TO_SEND = 'test.jpg' 

def send_file():

    if not os.path.exists(FILE_TO_SEND):
        print(f"Error: {FILE_TO_SEND} not found.")
        return

    filesize = os.path.getsize(FILE_TO_SEND)

    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        print(f"Connecting to {HOST}:{PORT}...")
        s.connect((HOST, PORT))

        # 1. Send Metadata
        metadata = f"{FILE_TO_SEND}|{filesize}"
        s.sendall(metadata.encode())
        
        time.sleep(0.1) 

        # 2. Send File Content
        with open(FILE_TO_SEND, 'rb') as f:
            while True:
                bytes_read = f.read(1024)
                if not bytes_read:
                    break
                s.sendall(bytes_read)
        
        print(f"Sent {FILE_TO_SEND} successfully.")

if __name__ == "__main__":
    send_file()