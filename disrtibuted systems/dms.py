import threading
import time

# Shared dictionary representing shared memory with a single key 'x'
shared_memory = {'x': 0}

# A lock to synchronize access to shared_memory
lock = threading.Lock()

def write_thread(value, delay):
    # Wait for a specified delay before writing
    time.sleep(delay)
    # Acquire lock to safely write to shared memory
    with lock:
        shared_memory['x'] = value
        print(f"Written: {value}")

def read_thread(delay):
    # Wait for a specified delay before reading
    time.sleep(delay)
    # Read shared memory without lock (may cause race condition)
    print(f"Read: {shared_memory['x']}")

# Start a thread that writes the value 5 after 1 second
writer = threading.Thread(target=write_thread, args=(5, 1))
writer.start()

# Start a thread that reads the value after 2 seconds
reader = threading.Thread(target=read_thread, args=(2,))
reader.start()

# Optional: wait for both threads to complete before program exits
writer.join()
reader.join()
