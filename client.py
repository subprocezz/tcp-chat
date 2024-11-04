import socket
import threading

def receive_messages(client_socket):
    while True:
        try:
            message = client_socket.recv(1024)
            if message:
                print(message.decode('utf-8'))
            else:
                print("The server has closed the connection.")
                break
        except ConnectionResetError:
            print("The server has closed the connection.")
            break
        except Exception as e:
            print(f"An error occurred while receiving the message: {e}")
            break

def start_client():
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    IP, PORT = 'localhost', 12345
    client_socket.connect((IP, PORT))
    
    threading.Thread(target=receive_messages, args=(client_socket,), daemon=True).start()

    while True:
        message = input()
        
        if message.lower() == '!exit':
            print("Disconnecting from the server ...")
            client_socket.close()
            break
        
        if message.strip():
            client_socket.send(message.encode('utf-8'))
        else:
            continue

if __name__ == "__main__":
    start_client()

