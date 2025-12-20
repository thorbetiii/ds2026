from mpi4py import MPI
import os

comm = MPI.COMM_WORLD
rank = comm.Get_rank()

FILE_TO_SEND = 'test.jpg'

if rank == 0:
    if not os.path.exists(FILE_TO_SEND):
        print(f"[Rank 0] Error: {FILE_TO_SEND} not found.")
    else:
        print(f"[Rank 0] Found file. Preparing to send to Rank 1...")
        
        with open(FILE_TO_SEND, 'rb') as f:
            file_data = f.read()

        data_package = {
            'filename': FILE_TO_SEND,
            'content': file_data
        }
        
        comm.send(data_package, dest=1, tag=0)
        print(f"[Rank 0] Sent {len(file_data)} bytes to Rank 1.")

elif rank == 1:
    print("[Rank 1] Waiting for data...")
    
    received_package = comm.recv(source=0, tag=0)
    
    filename = received_package['filename']
    content = received_package['content']
    
    save_name = f"received_{filename}"
    with open(save_name, 'wb') as f:
        f.write(content)
        
    print(f"[Rank 1] Saved file as {save_name} successfully.")