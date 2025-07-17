import threading
import time
import random

class Server:
    def __init__(self):
        # Flag to indicate if the server is alive
        self.alive = True

    def heartbeat(self):
        # Continuously print heartbeat status while server is alive
        while self.alive:
            print("Server: alive")
            time.sleep(2)

class Monitor:
    def __init__(self, server):
        # Monitor takes a reference to the server to check its status
        self.server = server

    def check_heartbeat(self):
        # Check the server heartbeat 5 times
        for _ in range(5):
            # Randomly simulate server failure with 20% chance
            if random.random() < 0.2:
                self.server.alive = False  # Mark server as down

            time.sleep(3)  # Wait 3 seconds between checks

            # If server is down, notify and stop monitoring
            if not self.server.alive:
                print("Monitor: Server failure detected!")
                return

        # If loop completes without detecting failure, server is healthy
        print("Monitor: Server healthy.")

# Create server instance
server = Server()

# Create monitor instance linked to the server
monitor = Monitor(server)

# Start the server heartbeat in a separate thread
heartbeat_thread = threading.Thread(target=server.heartbeat)
heartbeat_thread.start()

# Run monitor check in the main thread
monitor.check_heartbeat()

# Optional: Wait for the heartbeat thread to end before exiting
heartbeat_thread.join()
