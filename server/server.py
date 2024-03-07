from flask import Flask, request
from flask_socketio import SocketIO, emit
from threading import Lock


app = Flask(__name__)
socketio = SocketIO(app)
thread_lock = Lock()

db =


clients = {}
# games = {}
games = []

#def match_players():
#    while True:
#        with thread_lock:
#            available_clients = [client_id for client_id, client in clients.items() if client['opponent'] is None]
#            while len(available_clients) >= 2:
#                print(f'Available clients: {available_clients}')
#                player1_id = random.choice(available_clients)
#                available_clients.remove(player1_id)
#                player2_id = random.choice(available_clients)
#                available_clients.remove(player2_id)
#                clients[player1_id]['opponent'] = player2_id
#                clients[player2_id]['opponent'] = player1_id
#                print(f'Game started between {player1_id} and {player2_id}')
#        socketio.sleep(10)

def evaluate_game(player1_choice, player2_choice):
    if player1_choice == player2_choice:
        return "Draw"
    elif (player1_choice == "rock" and player2_choice == "scissors") or \
         (player1_choice == "scissors" and player2_choice == "paper") or \
         (player1_choice == "paper" and player2_choice == "rock"):
        return "Player 1 wins"
    else:
        return "Player 2 wins"

@socketio.on('connect')
def handle_connect():
    #global match_task
    print(f'Client connected: {request.sid}')
    with thread_lock:
        clients[request.sid] = {"choice": None, "opponent": None}
    #if 'match_task' not in globals() or not match_task.is_alive():
    #    match_task = socketio.start_background_task(match_players)
    #    print("Match task started")


@socketio.on('disconnect')
def handle_disconnect():
    print(f'Client disconnected: {request.sid}')
    with thread_lock:
        #opponent_sid = clients[request.sid]["opponent"]
        game = next((game for game in games if request.sid in game), None)
        if game:
            opponent_sid = next((sid for sid in game if sid != request.sid), None)
            if opponent_sid:
                emit('opponent_disconnected', room=opponent_sid)
                clients[opponent_sid]["opponent"] = None
            games.remove(game)

        del clients[request.sid]

#@socketio.on('play')
#def handle_play(data):
#    choice = data['choice']
#    with thread_lock:
#        clients[request.sid]['choice'] = choice
#        opponent_sid = clients[request.sid]['opponent']
#        if opponent_sid and clients[opponent_sid]['choice'] is not None:
#            player1_sid = request.sid
#            player2_sid = opponent_sid
#            player1_choice = clients[player1_sid]['choice']
#            player2_choice = clients[player2_sid]['choice']
#            result = evaluate_game(player1_choice, player2_choice)
#            emit('result', {'result': result, 'your_choice': player1_choice, 'opponent_choice': player2_choice}, room=player1_sid)
#            emit('result', {'result': result, 'your_choice': player2_choice, 'opponent_choice': player1_choice}, room=player2_sid)
#            # Reset choices after announcing results
#            clients[player1_sid]['choice'] = None
#            clients[player2_sid]['choice'] = None


@socketio.on('play')
def handle_play(data):
    choice = data['choice']
    with thread_lock:
        # Find the game that this player is part of
        game = next((game for game in games if request.sid in game), None)
        print(game)
        if game is None:
            print(f'Player {request.sid} is not part of a game')
            # If the player is not part of a game, create a new game if there is no game with one player
            game_with_one_player = next((game for game in games if len(game) == 1), None)
            if game_with_one_player is None:
                print(f'Creating a new game for player {request.sid}')
                game = {request.sid: {'choice': choice}}
                games.append(game)

            else:
                print(f'Adding player {request.sid} to game {game_with_one_player}')
                game = game_with_one_player
                game[request.sid] = {'choice': choice}

        else:
            # If the player is part of a game, update their choice
            game[request.sid]['choice'] = choice
            clients[request.sid]['choice'] = choice

        # If the game has two players and both have made a choice, evaluate the game
        if len(game) == 2 and all('choice' in player and player['choice'] is not None for player in game.values()):
            player1_sid, player2_sid = list(game.keys())
            player1_choice = game[player1_sid]['choice']
            player2_choice = game[player2_sid]['choice']
            result = evaluate_game(player1_choice, player2_choice)
            emit('result', {'result': result, 'your_choice': player1_choice, 'opponent_choice': player2_choice}, room=player1_sid)
            emit('result', {'result': result, 'your_choice': player2_choice, 'opponent_choice': player1_choice}, room=player2_sid)
            # Reset choices after announcing results
            # for sid in game:
            #     game[sid]['choice'] = None

            del game


def store_results_in_db(result, player1_choice, player2_choice):
    print(f'Storing results in database: {result}, {player1_choice}, {player2_choice}')



if __name__ == '__main__':
    socketio.run(app, debug=True, host='0.0.0.0')
