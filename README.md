# OS_-ASS1

# README

## Readers-Writers Problem with Load Balancing

This program implements the Readers-Writers problem using multiple replicas to distribute the reading load, ensuring synchronization using Python's `threading` module.

### Requirements
- Python 3.x

### Running the Program
1. Ensure Python 3 is installed on your system.
2. Open a terminal or command prompt.
3. Navigate to the directory where the script is saved.
4. Run the script using:
   ```sh
   python readers_writers.py
   ```
5. The program will create multiple `replicaX.txt` files and a `logging.txt` file to track operations.
6. Observe the logs in `logging.txt` for details on read and write operations.

### Expected Output
- `replicaX.txt`: Stores the content of each replica.
- `logging.txt`: Logs readers' access to replicas and writer updates.

### Stopping the Program
- The writer runs indefinitely. Stop execution using `Ctrl+C` in the terminal.

