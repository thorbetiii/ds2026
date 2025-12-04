import os
from xmlrpc.server import SimpleXMLRPCServer

HOST = '127.0.0.1'
PORT = 65432

def save_file(filename, file_data):
    """
    Receives a filename and a binary data object.
    Writes the data to the disk.
    """
    print(f"Receiving file: {filename}...")
    
    
    try:
        with open("received_" + filename, "wb") as handle:
            handle.write(file_data.data)
        print(f"Successfully saved: received_{filename}")
        return True
    except Exception as e:
        print(f"Error saving file: {e}")
        return False

if __name__ == "__main__":
    print(f"RPC Server listening on {HOST}:{PORT}...")
    
    with SimpleXMLRPCServer((HOST, PORT), allow_none=True) as server:
        server.register_function(save_file, "save_file")
        
        try:
            server.serve_forever()
        except KeyboardInterrupt:
            print("\nServer stopping...")