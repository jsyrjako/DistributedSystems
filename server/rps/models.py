from rps import db, bcrypt
import click
from flask.cli import with_appcontext


class GameResult(db.Model):
    __tablename__ = 'gameresults'

    id = db.Column(db.Integer, primary_key=True)
    player1 = db.Column(db.String())
    player2 = db.Column(db.String())
    result = db.Column(db.String())
    timestamp = db.Column(db.DateTime, server_default=db.func.now())

    def __init__(self, id, player1, player2, result):
        self.id = id
        self.player1 = player1
        self.player2 = player2
        self.result = result

    def __repr__(self):
        return '<id {}>'.format(self.id)
    
    def __str__(self):
        return f"GameResult(id={self.id}, player1={self.player1}, player2={self.player2}, result={self.result})"
