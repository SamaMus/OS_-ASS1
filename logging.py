import threading
import time
import random
from collections import defaultdict

NUM_REPLICAS = 3
LOG_FILE = "log.txt"


replica_locks = [threading.Lock() for _ in range(NUM_REPLICAS)] 
# to ensure writer priority
writer_lock = threading.Lock()
# We keep track of readers per replica
reader_count = [0] * NUM_REPLICAS 
reader_count_lock = threading.Lock()


file_replicas = [f"file_replica_{i}.txt" for i in range(NUM_REPLICAS)]

for file in file_replicas:
    with open(file, "w") as f:
        f.write("Initial content\n")
