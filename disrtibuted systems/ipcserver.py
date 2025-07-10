import socket
import threading
import base64

def handle_client(conn, addr):
    """Handle individual client connections"""
    try:
        print(f"Connection from {addr} has been established.")
        
        while True:
            # Receive encrypted data from client
            encrypted_data = conn.recv(1024)
            if not encrypted_data:
                break
            
            # Decrypt the data using base64
            try:
                decrypted_data = base64.b64decode(encrypted_data).decode()
                print(f"Received from {addr}: {decrypted_data}")
            except Exception as e:
                print(f"Error decrypting data from {addr}: {e}")
                continue
            
            # Prepare response and encrypt it
            response = f"Hello from server! Received: {decrypted_data}"
            encrypted_response = base64.b64encode(response.encode())
            
            # Send encrypted response back to client
            conn.send(encrypted_response)
            
    except ConnectionResetError:
        print(f"Client {addr} disconnected unexpectedly.")
    except Exception as e:
        print(f"Error handling client {addr}: {e}")
    finally:
        print(f"Connection with {addr} closed.")
        conn.close()

def start_server():
    """Start the server and listen for multiple clients"""
    try:
        # Create socket
        server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        
        # Bind to localhost on port 12345
        server_socket.bind(('localhost', 12345))
        
        # Listen for up to 5 connections
        server_socket.listen(5)
        print("Server is listening on port 12345...")
        print("Waiting for clients to connect...")
        
        while True:
            try:
                # Accept incoming connection
                conn, addr = server_socket.accept()
                
                # Create a new thread to handle the client
                client_thread = threading.Thread(target=handle_client, args=(conn, addr))
                client_thread.daemon = True  # Dies when main thread dies
                client_thread.start()
                
            except KeyboardInterrupt:
                print("\nServer shutting down...")
                break
            except Exception as e:
                print(f"Error accepting connection: {e}")
                
    except Exception as e:
        print(f"Error starting server: {e}")
    finally:
        try:
            server_socket.close()
        except:
            pass

if __name__ == "__main__":
    start_server()
