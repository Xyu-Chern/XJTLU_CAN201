
from socket import *
import argparse

def start_client(ip, port):
    """
    Initialize the client, connect to the server, and handle the game interaction.
    
    :param ip: The IP address of the server to connect to.
    :param port: The port number of the server to connect to.
    """
    client_socket = socket(AF_INET, SOCK_STREAM)
    client_socket.connect((ip, port))
    print(f'Connected to server at {ip}:{port}')
    name = input('Enter your name: ')
    client_socket.send(name.encode())

    while True:
        message = client_socket.recv(1024).decode()
        print(message)
        if 'won' in message or 'Congratulations' in message:
            break
        if 'Your turn to guess' in message:
            guess = input("Enter your guess: ")
            client_socket.sendall(guess.encode())
    client_socket.close()

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('--ip', default='127.0.0.1', type=str)
    parser.add_argument('--port', default=42345, type=int)
    args = parser.parse_args()
    start_client(args.ip, args.port)