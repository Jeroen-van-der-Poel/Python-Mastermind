from flask import session
from Game import Game
from db_connection import db_connection


class Player:
    def __init__(self, username: str):
        if 'player' not in session:
            session['player'] = username
            rows = db_connection.select_query('SELECT * FROM User WHERE username = ?', [username])
            if len(rows) == 0:
                db_connection.query('INSERT INTO User VALUES(null, ?)', [username])
                rows = db_connection.select_query('SELECT * FROM User WHERE username = ?', [username])
            session['player_id'] = rows[0][0]

    @staticmethod
    def begin_game():
        return Game(session['player_id'], True)