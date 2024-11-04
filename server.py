import socket, threading, logging, re
from colorama import Fore, init; init()

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler("./log/app.log"),  
        logging.StreamHandler()  
    ]
)

MAX_MESSAGE_LENGTH = 256  
users = {}  

RED, YELLOW, GREEN, RESET = Fore.RED, Fore.YELLOW, Fore.GREEN, Fore.RESET

def sanitize_message(message: str) -> str:
    return re.sub(r'[^a-zA-Z0-9\s,.!?]', '', message)

def truncate_message(message: str) -> str:
    if len(message) > MAX_MESSAGE_LENGTH:
        return message[:MAX_MESSAGE_LENGTH - 3] + '...'
    return message

def register_user(username: str, password: str) -> str:
    if username in users:
        return "Username already exists."
    users[username] = password
    return "Registration successful."

def authenticate_user(username: str, password: str) -> bool:
    return users.get(username) == password

def broadcast(message, sender_socket, clients):
    for client in clients:
        try:
            client.send(message)
        except Exception as e:
            logging.error(f"{RED}Error sending message to client: {e}{RESET}")

def handle_client(client_socket, clients):
    authenticated = False
    username = ""

    while not authenticated: 

        try:
            client_socket.send(b"Enter 'register <username> <password>' to register or 'login <username> <password>' to login: ")
            response = client_socket.recv(1024).decode('utf-8').strip()
            logging.info(f"{GREEN}Received response: {response}{YELLOW}")

            parts = response.split()
            if len(parts) < 3:
                client_socket.send(b"Invalid command. Please use the correct format.\n")
                continue

            command, username, password = parts[0], parts[1], parts[2]

            if command == "register":
                logging.info(f"{YELLOW}Attempting to register user: {username}{RESET}")
                msg = register_user(username, password)
                client_socket.send(msg.encode('utf-8'))

            elif command == "login":
                logging.info(f"{YELLOW}Attempting to login user: {username}{RESET}")
                if authenticate_user(username, password):
                    authenticated = True
                    client_socket.send(b"Login successful!\n")
                else:
                    client_socket.send(b"Login failed. Please try again.\n")

        except Exception as e:
            logging.error(f"{RED}Error during authentication: {e}{RESET}")
            break

    try:
        while True:
            message = client_socket.recv(1024)
            if not message:
                break
            
            decoded_message = message.decode('utf-8')
            sanitized_message = sanitize_message(decoded_message)
            truncated_message = truncate_message(sanitized_message)
             
            broadcast(f"{username}: {truncated_message}".encode('utf-8'), client_socket, clients)
    except Exception as e:
        logging.error(f"{RED}Error while handling messages: {e}{RESET}")
    finally:
        client_socket.close()
        clients.remove(client_socket)
        logging.info(f"{YELLOW}{username} disconnected.{RESET}")

def start_server():
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    IP, PORT = 'localhost', 12345
    server_socket.bind((IP, PORT))
    server_socket.listen(5)
    logging.info(f"{GREEN}Server listening {IP}:{PORT}{RESET}")

    clients = []
    
    while True:
        try:
            client_socket, addr = server_socket.accept()
            logging.info(f"{GREEN}Connection from {addr}{RESET}")
            clients.append(client_socket)

            threading.Thread(target=handle_client, args=(client_socket, clients)).start()
        except Exception as e:
            logging.error(f"{RED}Error accepting connection: {e}{RESET}")

if __name__ == "__main__":
    start_server()

