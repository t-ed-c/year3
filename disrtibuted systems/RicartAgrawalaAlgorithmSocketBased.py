import socket
import threading
import json
import time
from RicartAgrawalaAlgorithmBasicNode import BasicNode, MessageType

class SocketNode(BasicNode):
    def __init__(self, id, port, other_nodes):
        super().__init__(id)
        self.port = port
        self.other_nodes = other_nodes  # List of (id, host, port) tuples
        self.socket = None
        self.running = True
        self.replies_received = 0
        
    def start(self):
        # Start server socket
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.socket.bind(('localhost', self.port))
        self.socket.listen(5)
        
        print(f"Node {self.id} started on port {self.port}")
        
        # Start listening thread
        listen_thread = threading.Thread(target=self.listen_for_messages)
        listen_thread.daemon = True
        listen_thread.start()
        
    def listen_for_messages(self):
        while self.running:
            try:
                client_socket, address = self.socket.accept()
                message_thread = threading.Thread(target=self.handle_message, args=(client_socket,))
                message_thread.daemon = True
                message_thread.start()
            except:
                break
                
    def handle_message(self, client_socket):
        try:
            data = client_socket.recv(1024).decode('utf-8')
            if data:
                message = json.loads(data)
                self.process_message(message)
        except Exception as e:
            print(f"Node {self.id} error handling message: {e}")
        finally:
            client_socket.close()
            
    def process_message(self, message):
        self.logical_clock = max(self.logical_clock, message['timestamp']) + 1
        
        if message['type'] == MessageType.REQUEST.value:
            self.handle_request(message)
        elif message['type'] == MessageType.REPLY.value:
            self.handle_reply(message)
            
    def handle_request(self, message):
        print(f"Node {self.id} received REQUEST from Node {message['from_id']} at timestamp {message['timestamp']}")
        
        if not self.requesting_cs:
            self.send_reply(message['from_id'])
        elif self.compare_requests(message['timestamp'], message['from_id']):
            self.send_reply(message['from_id'])
        else:
            print(f"Node {self.id} deferred reply to Node {message['from_id']}")
            
    def handle_reply(self, message):
        print(f"Node {self.id} received REPLY from Node {message['from_id']}")
        self.replies_received += 1
        
        if self.replies_received == len(self.other_nodes):
            self.enter_critical_section()
            
    def send_message(self, target_id, message_type, timestamp=None):
        if timestamp is None:
            timestamp = self.logical_clock
            
        for node_id, host, port in self.other_nodes:
            if node_id == target_id:
                try:
                    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                    client_socket.connect((host, port))
                    
                    message = {
                        'type': message_type.value,
                        'from_id': self.id,
                        'timestamp': timestamp
                    }
                    
                    client_socket.send(json.dumps(message).encode('utf-8'))
                    client_socket.close()
                    
                except Exception as e:
                    print(f"Error sending message to Node {target_id}: {e}")
                break
                
    def send_reply(self, target_id):
        print(f"Node {self.id} sending REPLY to Node {target_id}")
        self.send_message(target_id, MessageType.REPLY)
        
    def request_critical_section(self):
        self.requesting_cs = True
        self.replies_received = 0
        self.logical_clock += 1
        self.request_timestamp = self.logical_clock
        
        print(f"Node {self.id} requesting Critical Section at timestamp {self.request_timestamp}")
        
        for node_id, host, port in self.other_nodes:
            self.send_message(node_id, MessageType.REQUEST, self.request_timestamp)
            
    def enter_critical_section(self):
        print(f"Node {self.id} ENTERING Critical Section")
        time.sleep(1)  # Simulate work
        print(f"Node {self.id} EXITING Critical Section")
        self.requesting_cs = False
        
    def stop(self):
        self.running = False
        if self.socket:
            self.socket.close()

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
        node = SocketNode(node_id, port, other_nodes)
        nodes.append(node)
        
    # Start all nodes
    for node in nodes:
        node.start()
        
    time.sleep(1)
    
    # Test requests
    threading.Timer(1.0, nodes[0].request_critical_section).start()
    threading.Timer(1.5, nodes[1].request_critical_section).start()
    
    try:
        time.sleep(10)
    except KeyboardInterrupt:
        pass
        
    for node in nodes:
        node.stop()