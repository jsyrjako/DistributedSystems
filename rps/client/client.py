import socketio
import random

sio = socketio.Client()

rps_moves = ["rock", "paper", "scissors"]

@sio.event
def connect():
    print('Connected to the server.')

@sio.event
def disconnect():
    print('Disconnected from the server.')

@sio.event
def result(data):
    print(f"Game result: {data['result']}. Your choice was {data['your_choice']}, opponent chose {data['opponent_choice']}.")
    # After receiving the result, prompt for the next round
    play_game()

@sio.event
def opponent_disconnected():
    print('Your opponent has disconnected. Waiting for a new opponent.')

def play_game():
    # This function is called to start a new game or play the next round
    choice = input("Choose rock, paper, or scissors: ")
    if choice in rps_moves:
        sio.emit('play', {'choice': choice}, namespace='/')
    else:
        print("Invalid choice. Please choose rock, paper, or scissors.")
        play_game()

def random_choice():
    choice = random.choice(rps_moves)
    return choice

def main():
    try:
        sio.connect('http://server:5000', namespaces=['/'])
        print("Connected to the server. Waiting to play Rock-Paper-Scissors...")
        play_game()  # Start the first round of the game
        sio.wait()
    except KeyboardInterrupt:
        print("Game interrupted.")
    except socketio.exceptions.ConnectionError as e:
        print(f"Connection failed: {e}")
    finally:
        sio.disconnect()

if __name__ == '__main__':
    main()