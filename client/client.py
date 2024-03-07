import socketio
import random
import argparse
import time
import os
from dotenv import dotenv_values

sio = socketio.Client()

rps_moves = ["rock", "paper", "scissors"]
choice_mapping = {"r": "rock", "p": "paper", "s": "scissors"}
arguments = {"User": False}

config = dotenv_values(".env")
SERVER_URL = config['SERVER_URL']

@sio.event
def connect():
    print("Connected to the server.")


@sio.event
def disconnect():
    print("Disconnected from the server.")
    return


@sio.event
def result(data):
    print(
        f"Game result: {data['result']}. Your choice was {data['your_choice']}, opponent chose {data['opponent_choice']}. \n"
    )
    # After receiving the result, prompt for the next round
    time.sleep(5)
    play_game()


@sio.event
def opponent_disconnected():
    print("Your opponent has disconnected. Searching for a new opponent.")
    play_game()


def play_game():
    # This function is called to start a new game or play the next round
    choice = ""
    if arguments["User"]:
        while choice not in rps_moves:
            choice = input(
                "Choose rock (r), paper (p), or scissors (s) or quit q: "
            ).lower()
            if choice in choice_mapping:
                choice = choice_mapping[choice]
            if choice in [
                "quit",
                "exit",
                "q",
                "Q",
            ]:
                print("Exiting the game...")
                os._exit(0)
            if choice not in rps_moves:
                print("Invalid choice. Please choose rock, paper, or scissors.")
    else:
        print(f"NO USER ARGUMENTS")
        choice = random_choice()

    sio.emit("play", {"choice": choice})
    sio.wait()


def random_choice():
    choice = random.choice(rps_moves)
    return choice


def main():
    parser = argparse.ArgumentParser(description="Rock-Paper-Scissors game")
    parser.add_argument(
        "-k", "--kayttaja", action="store_true", help="Play RPS manually"
    )
    args = parser.parse_args()

    if args.kayttaja:
        arguments["User"] = True
    print("Starting RPS...")
    try:
        print("Connecting to the server port 5000...")
        sio.connect(SERVER_URL)
        print("Connected to the server. Waiting to play Rock-Paper-Scissors...")
        play_game()  # Start the first round of the game
        sio.wait()
    except KeyboardInterrupt:
        print("Game interrupted.")
    except socketio.exceptions.ConnectionError as e:
        print(f"Connection failed: {e}")
    finally:
        sio.disconnect()


if __name__ == "__main__":
    main()
