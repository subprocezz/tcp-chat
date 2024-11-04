# Chat Server and Client Documentation

## Overview

This project consists of a simple chat server and client implemented in Python. The server handles user registration and authentication, and it facilitates message broadcasting among connected clients. The client connects to the server, allows user interaction, and displays incoming messages.

## Requirements

To run this project, you need Python 3.x installed on your machine. You can install the required libraries using a `requirements.txt` file.

### Installation of Required Libraries

1. Install the required libraries using pip:

```bash
pip install -r requirements.txt
```

## Server Code (`server.py`)

### Description

The server script manages user registration and login, message sanitization, and broadcasting messages to all connected clients. It logs all events to both the console and a file named `app.log`.

### Key Functions

1. **`sanitize_message(message: str) -> str`**
   - Sanitizes incoming messages to remove unwanted characters.
   - Returns a cleaned string.

2. **`truncate_message(message: str) -> str`**
   - Truncates messages to a maximum length defined by `MAX_MESSAGE_LENGTH`.
   - Returns the truncated message.

3. **`register_user(username: str, password: str) -> str`**
   - Registers a new user if the username does not already exist.
   - Returns a success or error message.

4. **`authenticate_user(username: str, password: str) -> bool`**
   - Checks if the provided username and password match an existing user.
   - Returns `True` if authenticated, otherwise `False`.

5. **`broadcast(message, sender_socket, clients)`**
   - Sends a message to all connected clients except the sender.
   - Handles errors while sending messages.

6. **`handle_client(client_socket, clients)`**
   - Manages communication with a connected client.
   - Handles user authentication and message processing.

7. **`start_server()`**
   - Initializes the server and listens for incoming connections.
   - Accepts new clients and spawns a new thread for each client.

### Logging

Logs are written to `./log/app.log` and also displayed in the console. The log includes information about connections, registrations, logins, and errors.

### Running the Server

To run the server, execute the script:

```bash
python server.py
```

## Client Code (`client.py`)

### Description

The client script connects to the chat server, allows users to send messages, and displays incoming messages from other users.

### Key Functions

1. **`receive_messages(client_socket)`**
   - Listens for messages from the server and prints them to the console.
   - Handles connection errors.

2. **`start_client()`**
   - Connects to the chat server and starts listening for messages.
   - Prompts the user to input messages and sends them to the server.

### Running the Client

To run the client, execute the script:

```bash
python client.py
```

### Disconnecting

Users can type `!exit` to disconnect from the server gracefully.

## Log File (`log/app.log`)

The log file records server activity, including connection attempts, user registrations, logins, and disconnections. Each log entry includes a timestamp, log level, and message.

### Example Log Entries

```
2024-11-04 11:40:11,590 - INFO - Server listening localhost:12345
2024-11-04 11:40:15,901 - INFO - Connection from ('127.0.0.1', 58130)
2024-11-04 11:40:27,870 - INFO - Received response: register test password123
2024-11-04 11:40:27,871 - INFO - Attempting to register user: test
2024-11-04 11:40:36,171 - INFO - Received response: login test password123
2024-11-04 11:40:36,172 - INFO - Attempting to login user: test
2024-11-04 11:40:42,276 - INFO - test disconnected.
```

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.

## Conclusion

This chat application provides basic functionality for user authentication and messaging. The server manages client connections and user data while the client enables user interaction through a command-line interface. Future improvements could include more robust error handling, message encryption, and user interface enhancements.

---

### LICENSE (MIT)

You can create a `LICENSE` file in your project root with the following content:

```
MIT License

Copyright (c) [year] [Your Name]

Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation files (the "Software"), to deal in the Software without restriction, including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and to permit persons to whom the Software is furnished to do so, subject to the following conditions:

...

[Complete the rest of the MIT license text]
```
