"""
Distributed Mutual Exclusion using Ricart-Agrawala Algorithm
===========================================================

This implementation demonstrates a distributed mutual exclusion algorithm
using the Ricart-Agrawala algorithm with the following features:
1. Socket-based message passing between nodes
2. Network delay simulation and failure handling
3. Message retry logic for reliability
4. Queue-based deferred reply management
5. Logical clock synchronization
6. Statistics tracking for performance analysis

The Ricart-Agrawala algorithm ensures mutual exclusion in distributed systems
by requiring all nodes to give permission before a node can enter the critical section.
"""

import socket
import threading
import time
import json
import random
from queue import Queue
from collections import defaultdict

class Node:
    """
    Represents a node in the distributed system implementing Ricart-Agrawala algorithm.
    
    Each node can request access to the critical section and must receive permission
    from all other nodes before entering. The algorithm uses logical timestamps
    to order requests and ensure fairness.
    """
    
    def __init__(self, node_id, port, peers):
        """
        Initialize a node in the distributed system.
        
        Args:
            node_id (int): Unique identifier for this node
            port (int): Port number for this node's socket server
            peers (dict): Dictionary mapping peer node IDs to their port numbers
        """
        self.id = node_id
        self.port = port
        self.peers = peers
        
        # Ricart-Agrawala algorithm state variables
        self.logical_clock = 0              # Lamport logical clock
        self.in_critical_section = False    # True when node is in CS
        self.requesting_cs = False          # True when node is requesting CS
        self.request_timestamp = None       # Timestamp of current CS request
        
        # Queue management for deferred replies
        self.deferred_replies = Queue()     # Queue of nodes waiting for replies
        self.pending_replies = set()        # Set of nodes we're waiting replies from
        
        # Message reliability features
        self.max_retries = 3                # Maximum retry attempts for failed messages
        self.retry_delay = 1.0              # Delay between retry attempts (seconds)
        
        # Performance statistics tracking
        self.stats = {
            'cs_entries': 0,        # Number of times this node entered CS
            'messages_sent': 0,     # Total messages sent (successful)
            'messages_failed': 0,   # Total messages that failed
            'messages_retried': 0,  # Total retry attempts
            'deferred_replies': 0   # Total replies deferred
        }
        
        # Network socket setup for inter-node communication
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.socket.bind(('localhost', self.port))
        self.socket.listen(3)  # Allow up to 3 pending connections
        
        # Network failure simulation parameters
        self.failure_rate = 0.2  # 20% chance of message failure
        
        self.running = True
        print(f"Node {self.id} started on port {self.port}")
    
    def start(self):
        """
        Start the node's message listener thread.
        
        Creates a daemon thread that continuously listens for incoming
        messages from other nodes in the distributed system.
        """
        listener_thread = threading.Thread(target=self.listen_for_messages)
        listener_thread.daemon = True  # Thread will exit when main program exits
        listener_thread.start()
    
    def listen_for_messages(self):
        """
        Continuously listen for incoming socket connections and process messages.
        
        This method runs in a separate thread and handles all incoming
        communication from peer nodes. It processes REQUEST and REPLY messages
        according to the Ricart-Agrawala protocol.
        """
        while self.running:
            try:
                # Accept incoming connection from a peer node
                client_socket, addr = self.socket.accept()
                
                # Receive and decode the JSON message
                data = client_socket.recv(1024).decode()
                if data:
                    message = json.loads(data)
                    self.process_message(message)
                client_socket.close()
                
            except socket.error as e:
                if self.running:  # Only log errors if not shutting down
                    print(f"Node {self.id}: Socket error in listener: {e}")
            except json.JSONDecodeError:
                print(f"Node {self.id}: Received invalid JSON message")
            except Exception as e:
                if self.running:
                    print(f"Node {self.id}: Error in message listener: {e}")
    
    def process_message(self, message):
        """
        Process incoming messages according to Ricart-Agrawala protocol.
        
        Args:
            message (dict): JSON message containing type, sender_id, and optional timestamp
                          Types: 'REQUEST' (CS request) or 'REPLY' (CS permission)
        """
        msg_type = message['type']
        sender_id = message['sender_id']
        timestamp = message.get('timestamp', 0)
        
        # Update logical clock according to Lamport's algorithm
        # Clock = max(local_clock, received_timestamp) + 1
        self.logical_clock = max(self.logical_clock, timestamp) + 1
        
        if msg_type == 'REQUEST':
            print(f"Node {self.id} got REQUEST from Node {sender_id}")
            self.handle_request(sender_id, timestamp)
        elif msg_type == 'REPLY':
            print(f"Node {self.id} got REPLY from Node {sender_id}")
            self.handle_reply(sender_id)
    
    def handle_request(self, sender_id, sender_timestamp):
        """
        Handle Critical Section request from another node (Ricart-Agrawala core logic).
        
        Decision logic for replying to CS requests:
        1. If we're in CS: Defer the reply
        2. If we're requesting CS and our request has priority: Defer the reply
        3. Otherwise: Reply immediately
        
        Priority is determined by:
        - Lower timestamp wins
        - If timestamps are equal, lower node ID wins
        
        Args:
            sender_id (int): ID of the node requesting CS access
            sender_timestamp (int): Logical timestamp of the request
        """
        # Check if we should defer the reply
        should_defer = (
            self.in_critical_section or  # We're currently in CS
            (self.requesting_cs and      # We're also requesting CS AND
             (self.request_timestamp < sender_timestamp or  # Our request is older OR
              (self.request_timestamp == sender_timestamp and self.id < sender_id)))  # Same time but lower ID
        )
        
        if should_defer:
            # Defer the reply - add sender to queue for later processing
            self.deferred_replies.put(sender_id)
            self.stats['deferred_replies'] += 1
            print(f"Node {self.id} defers reply to Node {sender_id}")
        else:
            # Reply immediately - sender can proceed
            self.send_reply(sender_id)
    
    def handle_reply(self, sender_id):
        """
        Handle REPLY message from another node.
        
        When we receive a reply, we remove that node from our pending replies set.
        If we have received replies from all nodes and we're requesting CS,
        we can enter the critical section.
        
        Args:
            sender_id (int): ID of the node sending the reply
        """
        if sender_id in self.pending_replies:
            self.pending_replies.remove(sender_id)
            
            # Check if we have all required permissions
            if len(self.pending_replies) == 0 and self.requesting_cs:
                self.enter_critical_section()
    
    def send_message(self, target_id, message):
        """
        Send a message to another node with failure simulation and network delays.
        
        This method simulates real-world network conditions including:
        - Random network delays (0.1-0.5 seconds)
        - Network failures (20% failure rate)
        - Connection timeouts
        - Connection refused errors
        
        Args:
            target_id (int): ID of the target node
            message (dict): Message to send (JSON serializable)
            
        Returns:
            bool: True if message sent successfully, False otherwise
        """
        # Simulate network latency with random delay
        time.sleep(random.uniform(0.1, 0.5))
        
        # Simulate network failure
        if random.random() < self.failure_rate:
            print(f"Node {self.id}: Message to Node {target_id} FAILED! (network failure)")
            self.stats['messages_failed'] += 1
            return False
        
        try:
            # Create socket connection to target node
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.settimeout(5.0)  # 5 second timeout for connection
            sock.connect(('localhost', self.peers[target_id]))
            
            # Send JSON-encoded message
            sock.send(json.dumps(message).encode())
            sock.close()
            
            self.stats['messages_sent'] += 1
            print(f"Node {self.id} sent {message['type']} to Node {target_id}")
            return True
            
        except socket.timeout:
            print(f"Node {self.id}: Timeout sending to Node {target_id}")
            return False
        except ConnectionRefusedError:
            print(f"Node {self.id}: Node {target_id} is not reachable")
            return False
        except Exception as e:
            print(f"Node {self.id}: Failed to send to Node {target_id}: {e}")
            return False
    
    def send_message_with_retry(self, target_id, message):
        """
        Send message with retry logic for improved reliability.
        
        Critical messages (like CS requests and replies) are retried multiple times
        to handle temporary network failures and improve system reliability.
        
        Args:
            target_id (int): ID of the target node
            message (dict): Message to send
            
        Returns:
            bool: True if message eventually sent successfully, False if all retries failed
        """
        for attempt in range(self.max_retries):
            if self.send_message(target_id, message):
                return True
                
            # Track retry statistics
            self.stats['messages_retried'] += 1
            
            # Wait before retrying (except on last attempt)
            if attempt < self.max_retries - 1:
                print(f"Node {self.id}: Retrying message to Node {target_id} (attempt {attempt + 2})")
                time.sleep(self.retry_delay)
                
        print(f"Node {self.id}: Failed to send message to Node {target_id} after {self.max_retries} attempts")
        return False
    
    def send_reply(self, target_id):
        """
        Send a REPLY message to grant CS permission to another node.
        
        Uses retry logic to ensure the reply reaches the requesting node,
        as failed replies can cause deadlock in the mutual exclusion algorithm.
        
        Args:
            target_id (int): ID of the node to send the reply to
        """
        message = {'type': 'REPLY', 'sender_id': self.id}
        threading.Thread(target=self.send_message_with_retry, args=(target_id, message)).start()
    
    def request_critical_section(self):
        """
        Request access to the critical section using Ricart-Agrawala protocol.
        
        Protocol steps:
        1. Increment logical clock
        2. Set request timestamp
        3. Send REQUEST message to all peer nodes
        4. Wait for REPLY from all peers before entering CS
        
        If already in CS or requesting CS, the request is ignored.
        """
        # Prevent multiple simultaneous requests from same node
        if self.in_critical_section or self.requesting_cs:
            return
        
        # Step 1: Increment logical clock for new request
        self.logical_clock += 1
        self.request_timestamp = self.logical_clock
        self.requesting_cs = True
        
        # Step 2: Initialize set of nodes we need replies from
        self.pending_replies = set(self.peers.keys())
        
        print(f"Node {self.id} requests CS at time {self.request_timestamp}")
        
        # Step 3: Send REQUEST to all peer nodes with retry logic
        message = {'type': 'REQUEST', 'sender_id': self.id, 'timestamp': self.request_timestamp}
        for peer_id in self.peers:
            threading.Thread(target=self.send_message_with_retry, args=(peer_id, message)).start()
    
    def enter_critical_section(self):
        """
        Enter the critical section after receiving permission from all nodes.
        
        This method is called automatically when all required REPLY messages
        have been received. It simulates work in the critical section and
        then automatically exits.
        """
        self.in_critical_section = True
        self.requesting_cs = False
        self.stats['cs_entries'] += 1
        
        print(f">>> Node {self.id} ENTERS Critical Section")
        
        # Simulate work in critical section
        time.sleep(2)  # 2 seconds of "critical work"
        
        print(f">>> Node {self.id} EXITS Critical Section")
        
        self.exit_critical_section()
    
    def exit_critical_section(self):
        """
        Exit the critical section and send all deferred replies.
        
        When exiting CS, we must send REPLY messages to all nodes
        whose requests we deferred while we were in the critical section.
        This ensures progress and prevents deadlock.
        """
        self.in_critical_section = False
        
        # Send all deferred replies from the queue
        while not self.deferred_replies.empty():
            node_id = self.deferred_replies.get()
            self.send_reply(node_id)
    
    def get_statistics(self):
        """
        Get a copy of the node's performance statistics.
        
        Returns:
            dict: Copy of statistics dictionary with performance metrics
        """
        return self.stats.copy()
    
    def print_statistics(self):
        """
        Display comprehensive statistics about this node's performance.
        
        Shows metrics including:
        - Number of critical section entries
        - Message transmission statistics
        - Success rates and reliability metrics
        """
        print(f"\nNode {self.id} Statistics:")
        print(f"  Critical Section Entries: {self.stats['cs_entries']}")
        print(f"  Messages Sent: {self.stats['messages_sent']}")
        print(f"  Messages Failed: {self.stats['messages_failed']}")
        print(f"  Messages Retried: {self.stats['messages_retried']}")
        print(f"  Deferred Replies: {self.stats['deferred_replies']}")
        
        # Calculate and display success rate
        if self.stats['messages_sent'] > 0:
            success_rate = ((self.stats['messages_sent'] - self.stats['messages_failed']) / self.stats['messages_sent']) * 100
            print(f"  Message Success Rate: {success_rate:.1f}%")

    def shutdown(self):
        """
        Gracefully shutdown the node and close all network connections.
        
        This method stops the message listener thread and closes the server socket.
        It's designed to handle shutdown errors gracefully.
        """
        print(f"Node {self.id}: Shutting down...")
        self.running = False
        try:
            self.socket.close()
        except:
            pass  # Ignore errors during shutdown

# Enhanced test with better monitoring
def test_algorithm():
    """
    Comprehensive test of the Ricart-Agrawala mutual exclusion algorithm.
    
    This test demonstrates various scenarios:
    1. Concurrent requests from multiple nodes
    2. Sequential requests to test fairness
    3. High contention scenarios with rapid requests
    
    The test includes monitoring and statistics to analyze algorithm performance
    under different conditions including network failures and delays.
    """
    print("=" * 60)
    print("ENHANCED RICART-AGRAWALA MUTUAL EXCLUSION TEST")
    print("Features: Sockets + Delays + Failure + Queue + Retry Logic")
    print("=" * 60)
    
    # Create 3 nodes with different ports
    # Each node knows about the other nodes' ports for communication
    nodes = {
        1: Node(1, 5001, {2: 5002, 3: 5003}),  # Node 1 on port 5001
        2: Node(2, 5002, {1: 5001, 3: 5003}),  # Node 2 on port 5002
        3: Node(3, 5003, {1: 5001, 2: 5002})   # Node 3 on port 5003
    }
    
    # Start message listeners for all nodes
    for node in nodes.values():
        node.start()
    
    # Wait for all nodes to be ready
    time.sleep(1)
    
    # Test Round 1: Concurrent Critical Section Requests
    print("\n" + "=" * 40)
    print("ROUND 1: Concurrent CS requests")
    print("=" * 40)
    print("Testing algorithm behavior when multiple nodes request CS simultaneously...")
    
    # All nodes request CS at nearly the same time
    nodes[1].request_critical_section()
    time.sleep(0.1)  # Small delay between requests
    nodes[2].request_critical_section()
    time.sleep(0.1)  
    nodes[3].request_critical_section()
    
    # Allow time for message exchange and CS execution
    time.sleep(10)
    
    # Test Round 2: Sequential Requests
    print("\n" + "=" * 40)
    print("ROUND 2: Sequential CS requests")
    print("=" * 40)
    print("Testing fairness with sequential requests...")
    
    nodes[3].request_critical_section()
    time.sleep(0.1)
    nodes[1].request_critical_section()
    
    time.sleep(8)
    
    # Test Round 3: High Contention Scenario
    print("\n" + "=" * 40)
    print("ROUND 3: High contention scenario")
    print("=" * 40)
    print("Testing algorithm under high load with rapid successive requests...")
    
    # Multiple rounds of rapid requests from all nodes
    for i in range(3):
        print(f"Contention round {i+1}/3")
        nodes[1].request_critical_section()
        time.sleep(0.05)  # Very short delays
        nodes[2].request_critical_section()
        time.sleep(0.05)
        nodes[3].request_critical_section()
        time.sleep(2)  # Wait between rounds
    
    # Allow final requests to complete
    time.sleep(5)
    
    print("\n" + "=" * 40)
    print("TEST COMPLETED - Shutting down nodes")
    print("=" * 40)
    
    # Display performance statistics for analysis
    print("\n" + "=" * 50)
    print("FINAL STATISTICS")
    print("=" * 50)
    for node in nodes.values():
        node.print_statistics()
    
    # Clean shutdown of all nodes
    for node in nodes.values():
        node.shutdown()
    
    time.sleep(1)
    print("\nAll nodes shut down successfully!")


# Main execution block
if __name__ == "__main__":
    """
    Main execution entry point.
    
    Runs the comprehensive test of the Ricart-Agrawala algorithm with
    proper error handling for user interruption and unexpected errors.
    """
    try:
        test_algorithm()
    except KeyboardInterrupt:
        print("\nTest interrupted by user")
    except Exception as e:
        print(f"\nError during test: {e}")
    finally:
        print("Test completed.")