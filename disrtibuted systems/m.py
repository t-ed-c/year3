import socket
import threading
import time
import json
import random
from queue import Queue

class Node:
    def __init__(self, node_id, port, peers):
        self.id = node_id
        self.port = port
        self.peers = peers
        
        # Algorithm state
        self.logical_clock = 0
        self.in_critical_section = False
        self.requesting_cs = False
        self.request_timestamp = None
        
        # Queue for deferred replies
        self.deferred_replies = Queue()
        self.pending_replies = set()
        
        # Socket setup
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.socket.bind(('localhost', self.port))
        self.socket.listen(3)
        
        # Failure simulation (simplified)
        self.failure_rate = 0.2  # 20% failure chance
        
        self.running = True
        print(f"Node {self.id} started on port {self.port}")
    
    def start(self):
        """Start the node's message listener"""
        listener_thread = threading.Thread(target=self.listen_for_messages)
        listener_thread.daemon = True
        listener_thread.start()
    
    def listen_for_messages(self):
        """Listen for incoming messages from other nodes"""
        while self.running:
            try:
                client_socket, addr = self.socket.accept()
                # Handle message directly (simplified)
                data = client_socket.recv(1024).decode()
                if data:
                    message = json.loads(data)
                    self.process_message(message)
                client_socket.close()
            except:
                pass
    
    def process_message(self, message):
        """Process received messages"""
        msg_type = message['type']
        sender_id = message['sender_id']
        timestamp = message.get('timestamp', 0)
        
        # Update logical clock
        self.logical_clock = max(self.logical_clock, timestamp) + 1
        
        if msg_type == 'REQUEST':
            print(f"Node {self.id} got REQUEST from Node {sender_id}")
            self.handle_request(sender_id, timestamp)
        elif msg_type == 'REPLY':
            print(f"Node {self.id} got REPLY from Node {sender_id}")
            self.handle_reply(sender_id)
    
    def handle_request(self, sender_id, sender_timestamp):
        """Handle CS request from another node"""
        if self.in_critical_section or (self.requesting_cs and 
           (self.request_timestamp < sender_timestamp or 
            (self.request_timestamp == sender_timestamp and self.id < sender_id))):
            # Defer the reply (add to queue)
            self.deferred_replies.put(sender_id)
            print(f"Node {self.id} defers reply to Node {sender_id}")
        else:
            # Reply immediately
            self.send_reply(sender_id)
    
    def handle_reply(self, sender_id):
        """Handle reply from another node"""
        if sender_id in self.pending_replies:
            self.pending_replies.remove(sender_id)
            if len(self.pending_replies) == 0 and self.requesting_cs:
                self.enter_critical_section()
    
    def send_message(self, target_id, message):
        """Send message with failure simulation and delays"""
        # Add delay
        time.sleep(random.uniform(0.1, 0.5))
        
        # Simulate failure
        if random.random() < self.failure_rate:
            print(f"Node {self.id}: Message to {target_id} FAILED!")
            return
        
        try:
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.connect(('localhost', self.peers[target_id]))
            sock.send(json.dumps(message).encode())
            sock.close()
            print(f"Node {self.id} sent {message['type']} to Node {target_id}")
        except:
            print(f"Node {self.id}: Failed to send to Node {target_id}")
    
    def send_reply(self, target_id):
        """Send reply message"""
        message = {'type': 'REPLY', 'sender_id': self.id}
        threading.Thread(target=self.send_message, args=(target_id, message)).start()
    
    def request_critical_section(self):
        """Request access to critical section"""
        if self.in_critical_section or self.requesting_cs:
            return
        
        self.logical_clock += 1
        self.request_timestamp = self.logical_clock
        self.requesting_cs = True
        self.pending_replies = set(self.peers.keys())
        
        print(f"Node {self.id} requests CS at time {self.request_timestamp}")
        
        # Send REQUEST to all peers
        message = {'type': 'REQUEST', 'sender_id': self.id, 'timestamp': self.request_timestamp}
        for peer_id in self.peers:
            threading.Thread(target=self.send_message, args=(peer_id, message)).start()
    
    def enter_critical_section(self):
        """Enter critical section"""
        self.in_critical_section = True
        self.requesting_cs = False
        
        print(f">>> Node {self.id} ENTERS Critical Section")
        time.sleep(2)  # Simulate work
        print(f">>> Node {self.id} EXITS Critical Section")
        
        self.exit_critical_section()
    
    def exit_critical_section(self):
        """Exit critical section and send deferred replies"""
        self.in_critical_section = False
        
        # Send all deferred replies from queue
        while not self.deferred_replies.empty():
            node_id = self.deferred_replies.get()
            self.send_reply(node_id)
    
    def shutdown(self):
        """Shutdown node"""
        self.running = False
        self.socket.close()

# Simple test
def test_algorithm():
    """Simple test with 3 nodes"""
    nodes = {
        1: Node(1, 5001, {2: 5002, 3: 5003}),
        2: Node(2, 5002, {1: 5001, 3: 5003}),
        3: Node(3, 5003, {1: 5001, 2: 5002})
    }
    
    # Start all nodes
    for node in nodes.values():
        node.start()
    
    time.sleep(1)
    
    print("\nTesting Critical Section requests...")
    
    # Concurrent requests
    nodes[1].request_critical_section()
    time.sleep(0.1)
    nodes[2].request_critical_section()
    time.sleep(0.1)  
    nodes[3].request_critical_section()
    
    # Let it run
    time.sleep(8)
    
    # Second round
    print("\nSecond round...")
    nodes[3].request_critical_section()
    time.sleep(0.1)
    nodes[1].request_critical_section()
    
    time.sleep(6)
    
    # Cleanup
    for node in nodes.values():
        node.shutdown()

if __name__ == "__main__":
    print("Simplified Ricart-Agrawala Algorithm")
    print("Features: Sockets + Delays + Failure + Queue")
    test_algorithm()