
from socket import *
from threading import Thread
import random
import argparse
import time

# global variable
clients = []            # List to store all connected client sockets
checkpoint = True       # Flag to ensure the random number is generated only once
game_over = False       # Flag to indicate if the game has ended
current_turn = 0        # Index of the player whose turn it is to guess
players = []            # List to store player information (socket and index)
player_guesses = {}     # Dictionary to store each player's current guess
round_guesses = {}      # Dictionary to track if each player has guessed in the current round

def start_server(ip, port, n = 2):
    """
    Initialize the server, accept client connections, and start handler threads.
    
    :param ip: IP address to bind the server.
    :param port: Port number to bind the server.
    :param n: Number of clients to wait for before starting the game.
    """
    num_clients = 0
    server_socket = socket(AF_INET, SOCK_STREAM)
    server_socket.bind((ip, port))
    server_socket.listen(n)
    print(f'Server started on {ip}:{port}')
    while num_clients < n:
        connection_socket, client_address = server_socket.accept()
        print(f'Client connected: {client_address}')
        client_handler = Thread(target=handle_client, args=(connection_socket, client_address))
        num_clients += 1
        client_handler.start()

def handle_client(connection_socket, client_address):
    """
    Handle communication with a connected client, manage game flow for the client.
    
    :param connection_socket: The socket object for the connected client.
    :param client_address: The address of the connected client.
    """
    global true_number, checkpoint, current_turn, game_over, clients, players, player_guesses, round_guesses
    name = initializePlayer(connection_socket)
    wait()
    getRandomNum()

    waiting_message_sent = False
    prev_index = -1  

    # main loop
    while not game_over:
        yourindex = get_player_index(connection_socket)
        # sleep if not your turn
        if yourindex != prev_index:
            waiting_message_sent = False
            prev_index = yourindex  
        if current_turn != yourindex:
            if not waiting_message_sent:
                connection_socket.send('Waiting for your turn...'.encode())
                waiting_message_sent = True
            time.sleep(1)
            continue
        waiting_message_sent = False
        
        # get guess
        print(f"Prompting {name} to guess.")
        connection_socket.send('Your turn to guess: '.encode())
        try:
            guess = int(connection_socket.recv(1024).decode())
        except ValueError:
            connection_socket.send('Invalid input. Please enter a number.'.encode())
            continue

        player_guesses[connection_socket] = guess  
        round_guesses[yourindex] = True  
        
        # check if the guess equals the random number
        if checkGuessTrue(guess, connection_socket, name):
            break

        # update order
        if all(round_guesses.values()):
            update_player_order()
            round_guesses = {player['index']: False for player in players}
            current_turn = 0 
        else:
            current_turn = (current_turn + 1) % len(players)

    connection_socket.close()

def initializePlayer(connection_socket):
    """
    Initialize a new player by receiving their name and adding them to the game.
    
    :param connection_socket: The socket object for the connected client.
    :return: The name of the player.
    """
    name = connection_socket.recv(1024).decode()
    clients.append(connection_socket)

    player_info = {'socket': connection_socket, 'index': len(players)}
    players.append(player_info)

    print(f'Received name: {name}')
    connection_socket.send('Waiting for other players...'.encode())
    return name

def wait():
    """
    Wait until the required number of clients have connected.
    """
    while len(clients) < 2:  
        time.sleep(1)

def getRandomNum():
    """
    Generate the random number to be guessed if it hasn't been generated yet,
    and notify all clients that the game has started.
    """
    global checkpoint, true_number, round_guesses
    if checkpoint:
        checkpoint = False
        true_number = random.randint(1, 100) # include 1-100
        print('All clients are ready. Starting the game.')
        print(f"Random number generated: {true_number}")
        for client in clients:
            client.send('Game started!'.encode())
        round_guesses = {i: False for i in range(len(clients))}

def checkGuessTrue(guess, connection_socket, name):
    """
    Check if the player's guess is correct, too high, or too low, and broadcast the result.
    
    :param guess: The number guessed by the player.
    :param connection_socket: The socket object for the connected client.
    :param name: The name of the player.
    :return: True if the guess is correct, False otherwise.
    """
    global true_number, game_over
    if guess == true_number:
        connection_socket.send('Congratulations! You guessed the number!'.encode())
        game_over = True
        broadcast(connection_socket, f'{name} guessed {guess} and won the game!'.encode())
        print(f'Received guess {guess} from {name}. {name} wins!')
        return True
    else:
        if guess < true_number:
            connection_socket.send('Your guess is too low.'.encode())
            broadcast(connection_socket, f'{name} guessed {guess}. The guess is too low.'.encode())
            print(f'Received guess {guess} from {name}. Too low.')
        else:
            connection_socket.send('Your guess is too high.'.encode())
            broadcast(connection_socket, f'{name} guessed {guess}. The guess is too high.'.encode())
            print(f'Received guess {guess} from {name}. Too high.')
        return False

def broadcast(connection_socket, message):
    """
    Send a message to all connected clients except the one specified.
    
    :param connection_socket: The socket to exclude from broadcasting.
    :param message: The message to send to the other clients.
    """
    for client in clients:
        if client != connection_socket:
            client.send(message)

def get_player_index(connection_socket):
    """
    Retrieve the index of the player based on their connection socket.
    
    :param connection_socket: The socket object for the connected client.
    :return: The index of the player or -1 if not found.
    """
    for player in players:
        if player['socket'] == connection_socket:
            return player['index']
    return -1  

def update_player_order():
    """
    Update the order of players based on how close their last guess was to the true number.
    Players who guessed closer to the true number will get priority in the next round.
    """
    global player_guesses, true_number, players
    distances = []
    for player in players:
        guess = player_guesses.get(player['socket'], None)
        if guess is not None:
            distance = abs(guess - true_number)
            distances.append((player, distance))
        else:
            distances.append((player, float('inf')))
    distances.sort(key=lambda x: x[1])
    players = [player for player, _ in distances]
    for idx, player in enumerate(players):
        player['index'] = idx

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('--ip', default='127.0.0.1', type=str)
    parser.add_argument('--port', default=42345, type=int)
    args = parser.parse_args()
    start_server(args.ip, args.port)

