from mpi4py import MPI

comm = MPI.COMM_WORLD
rank = comm.Get_rank()
size = comm.Get_size()

data = [
    "C:/Users/Admin/Documents/usth/b3/distributed_system/ds2026/Practical Work 1/server.py",
    "C:/Users/Admin/Documents/usth/b3/distributed_system/ds2026/Practical Work 2/RPC/client.py",
    "C:/Windows/System32/drivers/etc/hosts",
    "C:/Program Files/Python310/python.exe",
    "C:/Users/Admin/AppData/Local/MiKTeX/miktex/log/latexmk.log"
]

if rank == 0:
    chunks = [data[i::size] for i in range(size)]
else:
    chunks = None

my_paths = comm.scatter(chunks, root=0)

local_longest = ""
if my_paths:
    local_longest = max(my_paths, key=len)

all_candidates = comm.gather(local_longest, root=0)

if rank == 0:
    final_winner = max(all_candidates, key=len)
    
    print("\n--- MapReduce Longest Path Results ---")
    print(f"Longest Path Found: {final_winner}")
    print(f"Character Length: {len(final_winner)}")