import socket
import threading

def receive_messages(client_socket, username):
    while True:
        try:
            message = client_socket.recv(1024).decode('utf-8')
            if message.startswith(username + ": "):
                print(f"You: {message[len(username)+2:]}")
            else:
                print(message)
        except:
            print("Disconnected from server")
            client_socket.close()
            break

def start_client():
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_socket.connect(('localhost', 5555))
    
    username = input("Enter username: ")
    client_socket.send(username.encode('utf-8'))
    
    response = client_socket.recv(1024).decode('utf-8')
    print(response)
    
    if "taken" in response:
        return
    
    receive_thread = threading.Thread(target=receive_messages, args=(client_socket, username))
    receive_thread.start()
    
    try:
        while True:
            message = input()
            if message.lower() == 'exit':
                break
            client_socket.send(message.encode('utf-8'))
    finally:
        client_socket.close()

if __name__ == "__main__":
    start_client()
