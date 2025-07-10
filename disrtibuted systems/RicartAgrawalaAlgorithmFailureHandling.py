import json
import socket
import threading
import time
import random
from RicartAgrawalaAlgorithmSocketBased import SocketNode, MessageType

class ReliableNode(SocketNode):
    def __init__(self, id, port, other_nodes, failure_rate=0.1):
        super().__init__(id, port, other_nodes)
        self.failure_rate = failure_rate
        self.failed_nodes = set()
        self.timeout_duration = 5
        
    def handle_message(self, client_socket):
        try:
            # Simulate message processing delay
            time.sleep(random.uniform(0.1, 0.5))
            
            data = client_socket.recv(1024).decode('utf-8')
            if data:
                message = json.loads(data)
                self.process_message(message)
        except Exception as e:
            print(f"Node {self.id} error handling message: {e}")
        finally:
            client_socket.close()
            
    def send_message(self, target_id, message_type, timestamp=None, retry_count=0):
        if timestamp is None:
            timestamp = self.logical_clock
            
        # Simulate message failure
        if random.random() < self.failure_rate:
            print(f"Node {self.id} -> Node {target_id}: Message {message_type.value} FAILED")
            if retry_count < 3:
                threading.Timer(1.0, lambda: self.send_message(target_id, message_type, timestamp, retry_count + 1)).start()
            else:
                print(f"Node {self.id} -> Node {target_id}: Message FAILED after 3 retries")
                self.failed_nodes.add(target_id)
            return False
            
        for node_id, host, port in self.other_nodes:
            if node_id == target_id:
                try:
                    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                    client_socket.settimeout(self.timeout_duration)
                    client_socket.connect((host, port))
                    
                    message = {
                        'type': message_type.value,
                        'from_id': self.id,
                        'timestamp': timestamp
                    }
                    
                    client_socket.send(json.dumps(message).encode('utf-8'))
                    client_socket.close()
                    
                    print(f"Node {self.id} -> Node {target_id}: {message_type.value} sent")
                    return True
                    
                except socket.timeout:
                    print(f"Node {self.id} -> Node {target_id}: TIMEOUT")
                    self.failed_nodes.add(target_id)
                    return False
                except Exception as e:
                    print(f"Node {self.id} -> Node {target_id}: Error - {e}")
                    self.failed_nodes.add(target_id)
                    return False
                break
        return False
        
    def request_critical_section(self):
        self.requesting_cs = True
        self.replies_received = 0
        self.logical_clock += 1
        self.request_timestamp = self.logical_clock
        
        print(f"Node {self.id} requesting Critical Section at timestamp {self.request_timestamp}")
        
        for node_id, host, port in self.other_nodes:
            if node_id not in self.failed_nodes:
                self.send_message(node_id, MessageType.REQUEST, self.request_timestamp)
            else:
                print(f"Node {self.id} skipping failed Node {node_id}")
                
        # Set timeout for CS request
        threading.Timer(self.timeout_duration * 2, self.handle_cs_timeout).start()
        
    def handle_cs_timeout(self):
        if self.requesting_cs:
            print(f"Node {self.id} CS request TIMED OUT")
            active_nodes = len([n for n in self.other_nodes if n[0] not in self.failed_nodes])
            if self.replies_received >= active_nodes:
                self.enter_critical_section()
            else:
                print(f"Node {self.id} cancelling CS request due to timeout")
                self.requesting_cs = False

# Example usage
if __name__ == "__main__":
    nodes_config = [
        (1, 'localhost', 8001),
        (2, 'localhost', 8002),
        (3, 'localhost', 8003)
    ]
    
    nodes = []
    for i, (node_id, host, port) in enumerate(nodes_config):
        other_nodes = [config for j, config in enumerate(nodes_config) if i != j]
        failure_rate = 0.3 if node_id == 3 else 0.1  # Node 3 has higher failure rate
        node = ReliableNode(node_id, port, other_nodes, failure_rate)
        nodes.append(node)
        
    # Start all nodes
    for node in nodes:
        node.start()
        
    time.sleep(1)
    
    # Test with failures
    threading.Timer(1.0, nodes[0].request_critical_section).start()
    threading.Timer(2.0, nodes[1].request_critical_section).start()
    
    try:
        time.sleep(15)
    except KeyboardInterrupt:
        pass
        
    for node in nodes:
        node.stop()