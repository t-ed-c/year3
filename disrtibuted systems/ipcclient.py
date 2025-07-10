import socket
import base64

def send_message(message):
    """Send an encrypted message to the server"""
    try:
        # Create socket
        client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        
        # Connect to server
        print("Connecting to server...")
        client_socket.connect(('localhost', 12345))
        print("Connected to server successfully!")
        
        # Encrypt the message using base64
        encrypted_message = base64.b64encode(message.encode())
        
        # Send encrypted message
        client_socket.send(encrypted_message)
        print(f"Sent encrypted message: {message}")
        
        # Receive encrypted response
        encrypted_response = client_socket.recv(1024)
        
        if encrypted_response:
            # Decrypt the response
            try:
                decrypted_response = base64.b64decode(encrypted_response).decode()
                print(f"Received from server: {decrypted_response}")
            except Exception as e:
                print(f"Error decrypting server response: {e}")
        else:
            print("No response received from server.")
            
    except ConnectionRefusedError:
        print("Error: Could not connect to server. Make sure the server is running.")
    except socket.timeout:
        print("Error: Connection timed out.")
    except Exception as e:
        print(f"Error communicating with server: {e}")
    finally:
        try:
            client_socket.close()
            print("Connection closed.")
        except:
            pass

def main():
    """Main function to run the client"""
    try:
        # Get message from user
        message = input("Enter message to send to server (or 'quit' to exit): ")
        
        if message.lower() == 'quit':
            print("Goodbye!")
            return
            
        # Send message to server
        send_message(message)
        
    except KeyboardInterrupt:
        print("\nClient interrupted by user.")
    except Exception as e:
        print(f"Unexpected error: {e}")

if __name__ == "__main__":
    main()

# This code connects to a server running on localhost at port 12345, sends an encrypted message