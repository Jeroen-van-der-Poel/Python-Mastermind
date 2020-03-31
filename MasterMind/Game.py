from flask import session
from db_connection import db_connection


class Game:
    def __init__(self, player_id: int, newgame: bool):
        session['answer'] = []
        session['amount'] = 4
        session['color_amount'] = 6
        if newgame:
            db_connection.query("INSERT INTO Game(player_id)" +
                                'VALUES (?)', [player_id])
            result = db_connection.select_query('SELECT * FROM Game ' +
                                                'WHERE player_id = ?' +
                                                'ORDER BY created_at ' +
                                                'LIMIT 1', [player_id])
            session['game_id'] = result[0][0]
        else:
            pass

    def generateGame(amount: int, color_amount: int, is_double: bool):

        
