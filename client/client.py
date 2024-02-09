import socketio
import random
import argparse

sio = socketio.Client()

rps_moves = ["rock", "paper", "scissors"]
choice_mapping = {"r": "rock", "p": "paper", "s": "scissors"}

@sio.event
def connect():
    print("Connected to the server.")


@sio.event
def disconnect():
    print("Disconnected from the server.")


@sio.event
def result(data):
    print(
        f"Game result: {data['result']}. Your choice was {data['your_choice']}, opponent chose {data['opponent_choice']}."
    )
    # After receiving the result, prompt for the next round
    play_game()


@sio.event
def opponent_disconnected():
    print("Your opponent has disconnected. Waiting for a new opponent.")


def play_game(args=None):
    # This function is called to start a new game or play the next round
    choice = ""
    if args and args.user:
        while choice not in rps_moves:
            choice = input("Choose rock (r), paper (p), or scissors (s): ").lower()
            if choice in choice_mapping:
                choice = choice_mapping[choice]
            if choice not in rps_moves:
                print("Invalid choice. Please choose rock, paper, or scissors.")
    else:
        choice = random_choice()

    sio.emit("play", {"choice": choice}, namespace="/")


def random_choice():
    choice = random.choice(rps_moves)
    return choice


def main():
    parser = argparse.ArgumentParser(description="Rock-Paper-Scissors game")
    parser.add_argument("-u", "--user", action="store_true", help="Play RPS manually")
    args = parser.parse_args()

    try:
        sio.connect("http://server:5000", namespaces=["/"])
        print("Connected to the server. Waiting to play Rock-Paper-Scissors...")
        play_game(args)  # Start the first round of the game
        sio.wait()
    except KeyboardInterrupt:
        print("Game interrupted.")
    except socketio.exceptions.ConnectionError as e:
        print(f"Connection failed: {e}")
    finally:
        sio.disconnect()


if __name__ == "__main__":
    main()
