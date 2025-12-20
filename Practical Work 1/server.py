import socket
import os

HOST = '127.0.0.1'  
PORT = 65432        

def start_server():
    # Create a TCP/IP socket
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.bind((HOST, PORT))
        s.listen()
        print(f"Server listening on {HOST}:{PORT}")

        conn, addr = s.accept()
        with conn:
            print(f"Connected by {addr}")
            
            # 1. Receive Metadata (Filename|Filesize)
            received_data = conn.recv(1024).decode()
            filename, filesize = received_data.split('|')
            filesize = int(filesize)
            
            # Remove absolute path if sent, just keep filename
            filename = os.path.basename(filename) 
            
            print(f"Receiving file: {filename} ({filesize} bytes)")

            # 2. Receive File Data
            received_bytes = 0
            with open(f"received_{filename}", 'wb') as f:
                while received_bytes < filesize:
                    # Read 1024 bytes (or whatever is left)
                    chunk = conn.recv(1024)
                    if not chunk:
                        break
                    f.write(chunk)
                    received_bytes += len(chunk)

            print("File transfer complete.")

if __name__ == "__main__":
    start_server()