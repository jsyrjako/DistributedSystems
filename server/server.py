from flask import Flask, request
from flask_socketio import SocketIO, emit
from threading import Lock

app = Flask(__name__)
socketio = SocketIO(app)
thread_lock = Lock()

clients = {}
games = {}

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
    print(f'Client connected: {request.sid}')
    with thread_lock:
        clients[request.sid] = {"choice": None, "opponent": None}

@socketio.on('disconnect')
def handle_disconnect():
    print(f'Client disconnected: {request.sid}')
    with thread_lock:
        opponent_sid = clients[request.sid]["opponent"]
        if opponent_sid:
            emit('opponent_disconnected', room=opponent_sid)
            clients[opponent_sid]["opponent"] = None
        del clients[request.sid]

@socketio.on('play')
def handle_play(data):
    choice = data['choice']
    with thread_lock:
        clients[request.sid]['choice'] = choice
        if len(clients) == 2 and all(client['choice'] for client in clients.values()):
            player1_sid, player2_sid = list(clients.keys())
            player1_choice = clients[player1_sid]['choice']
            player2_choice = clients[player2_sid]['choice']
            result = evaluate_game(player1_choice, player2_choice)
            emit('result', {'result': result, 'your_choice': player1_choice, 'opponent_choice': player2_choice}, room=player1_sid)
            emit('result', {'result': result, 'your_choice': player2_choice, 'opponent_choice': player1_choice}, room=player2_sid)
            # Reset choices after announcing results
            for sid in clients:
                clients[sid]['choice'] = None

if __name__ == '__main__':
    socketio.run(app, debug=True, host='0.0.0.0')