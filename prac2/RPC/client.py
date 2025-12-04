import os
import xmlrpc.client

HOST = '127.0.0.1'
PORT = 65432
FILE_TO_SEND = 'test.jpg' 

def send_file_rpc():
    if not os.path.exists(FILE_TO_SEND):
        print(f"Error: '{FILE_TO_SEND}' not found. Please create it first.")
        return

    print(f"Connecting to RPC server at {HOST}:{PORT}...")

    proxy = xmlrpc.client.ServerProxy(f'http://{HOST}:{PORT}')

    try:
        with open(FILE_TO_SEND, "rb") as handle:
            binary_data = xmlrpc.client.Binary(handle.read())

        print(f"Sending '{FILE_TO_SEND}' via RPC...")
        
        result = proxy.save_file(FILE_TO_SEND, binary_data)

        if result:
            print("Server confirmed: File transfer successful!")
        else:
            print("Server reported a failure.")

    except ConnectionRefusedError:
        print("Error: Could not connect. Is the server running?")
    except Exception as e:
        print(f"An error occurred: {e}")

if __name__ == "__main__":
    send_file_rpc()