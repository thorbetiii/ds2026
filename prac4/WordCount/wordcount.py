from mpi4py import MPI
import collections

comm = MPI.COMM_WORLD
rank = comm.Get_rank()
size = comm.Get_size()

data = [
    "I dont want to learn French",
    "but French sound sexy",
    "python is usable for this lab"
]

if rank == 0:
    chunks = [data[i::size] for i in range(size)]
else:
    chunks = None

my_lines = comm.scatter(chunks, root=0)

my_counts = collections.defaultdict(int)
for line in my_lines:
    for word in line.lower().split():
        my_counts[word] += 1

all_counts = comm.gather(my_counts, root=0)

if rank == 0:
    final_counts = collections.defaultdict(int)
    for partial_dict in all_counts:
        for word, count in partial_dict.items():
            final_counts[word] += count

    print("--- Final Word Count Results ---")
    for word, count in sorted(final_counts.items(), key=lambda x: x[1], reverse=True):
        print(f"{word}: {count}")