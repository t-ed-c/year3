import time
from enum import Enum

class MessageType(Enum):
    REQUEST = "REQUEST"
    REPLY = "REPLY"

class BasicNode:
    def __init__(self, id):
        self.id = id
        self.logical_clock = 0
        self.requesting_cs = False
        self.request_timestamp = 0
        
    def request_cs(self, timestamp=None):
        if timestamp is None:
            self.logical_clock += 1
            timestamp = self.logical_clock
            
        self.requesting_cs = True
        self.request_timestamp = timestamp
        print(f"Node {self.id} requests CS at time {timestamp}")
        return f"REQ from {self.id} at {timestamp}"

    def receive_reply(self, from_id):
        print(f"Node {self.id} received REPLY from {from_id}")
        
    def send_reply(self, to_id):
        print(f"Node {self.id} sending REPLY to {to_id}")
        
    def compare_requests(self, other_timestamp, other_id):
        """Compare two requests based on timestamp and node ID"""
        if self.request_timestamp < other_timestamp:
            return True
        elif self.request_timestamp == other_timestamp:
            return self.id < other_id
        return False

# Example usage
if __name__ == "__main__":
    node1 = BasicNode(1)
    node2 = BasicNode(2)
    
    req1 = node1.request_cs(5)
    req2 = node2.request_cs(4)
    
    print(f"Request 1: {req1}")
    print(f"Request 2: {req2}")
    
    # Simulate priority comparison
    if node1.compare_requests(node2.request_timestamp, node2.id):
        print("Node 1 has higher priority")
        node2.receive_reply(1)
    else:
        print("Node 2 has higher priority")
        node1.receive_reply(2)