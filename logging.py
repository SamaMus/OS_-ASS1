import threading
import time
import random
from datetime import datetime

NUM_REPLICAS = 3
NUM_READERS = 10

# Shared data
readers_count = [0] * NUM_REPLICAS
replica_mutex = [threading.Lock() for _ in range(NUM_REPLICAS)]
reader_count_mutex = threading.Lock()
writer_mutex = threading.Lock()
log_mutex = threading.Lock()

def log_event(event):
    with log_mutex:
        with open("logging.txt", "a") as log_file:
            log_file.write(event + "\n")

def initialize_replicas():
    for i in range(NUM_REPLICAS):
        with open(f"replica{i+1}.txt", "w") as file:
            file.write(f"Initial content of replica{i+1}.txt\n")

def reader(reader_id):
    time.sleep(random.randint(1, 3))  # Simulate random arrival
    
    # Choose the least loaded replica
    with reader_count_mutex:
        file_index = min(range(NUM_REPLICAS), key=lambda i: readers_count[i])
        readers_count[file_index] += 1
    
    with replica_mutex[file_index]:
        with open(f"replica{file_index+1}.txt", "r") as file:
            content = file.read().strip()
        log_event(f"Operation: Reader {reader_id} read from replica{file_index+1}.txt: {content}")
        
    with reader_count_mutex:
        readers_count[file_index] -= 1
    
    log_event(f"Readers: {', '.join([f'replica{i+1}: {count}' for i, count in enumerate(readers_count)])}")

def writer():
    while True:
        time.sleep(random.randint(3, 6))  # Simulate periodic writes
        with writer_mutex:
            for lock in replica_mutex:
                lock.acquire()
            
            log_event("Operation: Writer updated all replicas.")
            timestamp = datetime.now().strftime("%a %b %d %H:%M:%S %Y")
            for i in range(NUM_REPLICAS):
                with open(f"replica{i+1}.txt", "w") as file:
                    file.write(f"Updated by writer at {timestamp}\n")
            log_event("Writer active: Yes")
            
            for lock in replica_mutex:
                lock.release()
            log_event("Writer active: No")

def main():
    random.seed()
    open("logging.txt", "w").close()  # Clear log file
    initialize_replicas()
    
    writer_thread = threading.Thread(target=writer, daemon=True)
    writer_thread.start()
    
    reader_threads = []
    for i in range(NUM_READERS):
        t = threading.Thread(target=reader, args=(i,))
        reader_threads.append(t)
        t.start()
        time.sleep(random.randint(1, 2))  # Randomized reader spawn
    
    for t in reader_threads:
        t.join()
    
if __name__ == "__main__":
    main()
