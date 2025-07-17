import os
import shutil

# List of simulated file server directories
servers = ['server1/', 'server2/']

def replicate_file(filename, content):
    # Write the file with given content to all servers (simulate replication)
    for server in servers:
        os.makedirs(server, exist_ok=True)  # Create server folder if it doesn't exist
        with open(server + filename, 'w') as f:
            f.write(content)  # Write content to the file on the server

def read_file(filename):
    cache_path = 'cache/' + filename  # Local cache path for the file

    # If file exists in local cache, read and return it
    if os.path.exists(cache_path):
        print("Reading from cache")
        with open(cache_path, 'r') as f:
            return f.read()

    # Otherwise, check each server for the file
    for server in servers:
        path = server + filename
        if os.path.exists(path):
            print(f"Reading from {server}")
            os.makedirs('cache', exist_ok=True)  # Ensure cache directory exists
            shutil.copy(path, cache_path)        # Copy file to local cache
            with open(path, 'r') as f:
                return f.read()

    # If file not found on any server or cache
    return "File not found."
# Test the system
replicate_file("example.txt", "This is a test content.")

print("\n--- First read (should come from server) ---")
print(read_file("example.txt"))

print("\n--- Second read (should come from cache) ---")
print(read_file("example.txt"))
