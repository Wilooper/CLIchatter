# CLIchatter
Want a private space for yourself ?Do private chatting using CLIchatter without tension of data and privacy issue.
Just clone this repositry in your system
In linux just run this command
https://github.com/Wilooper/CLIchatter.git
and then run 
cd CLIchatter
now run python3 server.py to start server
and then run client.py script to connect with server
share clent.py with your friend whome you want to chat and tell him to run it by using this command
python3 client.py
now chat freely without any privacy issue
import socket
import threading

clients = {}  # Maps usernames to client sockets

def handle_client(client_socket):
    username = None
    try:
        username = client_socket.recv(1024).decode('utf-8')
        if username in clients:
            client_socket.send("Username already taken!".encode('utf-8'))
            client_socket.close()
            return
        
        clients[username] = client_socket
        print(f"{username} connected")
        client_socket.send("Connected to server!".encode('utf-8'))

        while True:
            message = client_socket.recv(1024).decode('utf-8')
            if not message:
                break

            if message.startswith("/msg"):
                parts = message.split(' ', 2)
                if len(parts) < 3:
                    client_socket.send("Invalid PM format. Use: /msg recipient message".encode('utf-8'))
                    continue
                
                _, recipient, pm_content = parts
                if recipient in clients:
                    clients[recipient].send(f"[PM from {username}] {pm_content}".encode('utf-8'))
                    client_socket.send(f"[PM to {recipient}] {pm_content}".encode('utf-8'))
                else:
                    client_socket.send(f"User '{recipient}' not found".encode('utf-8'))
            else:
                broadcast_msg = f"{username}: {message}"
                print(broadcast_msg)
                for user in clients:
                    clients[user].send(broadcast_msg.encode('utf-8'))

    except Exception as e:
        print(f"Error: {e}")
    finally:
        if username and username in clients:
            del clients[username]
            print(f"{username} disconnected")
        client_socket.close()

def start_server():
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind(('localhost', 5555))
    server.listen()
    print("Server listening on port 5555...")
    
    while True:
        client_socket, addr = server.accept()
        thread = threading.Thread(target=handle_client, args=(client_socket,))
        thread.start()

if __name__ == "__main__":
    start_server()
