import random

from flask import session
from db_connection import db_connection
from Colors import Color


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
                                                'ORDER BY created_at DESC ' +
                                                'LIMIT 1', [player_id])
            session['game_id'] = result[0][0]
        else:
            pass


    @staticmethod
    def generate_game(amount: int, color_amount: int, is_double: bool):
        answer = session['answer']
        if 4 <= amount <= 10:
            session['amount'] = amount
        if 6 <= color_amount <= 10:
            if not color_amount >= amount:
                session['color_amount'] = amount
            else:
                session['color_amount'] = color_amount

        answer.clear()
        for i in range(session['color_amount']):
            answer.append(Color(i).label)
            session['colors'] = answer
        if is_double:
            answer = random_color(answer, amount)
        else:
            random.shuffle(answer)
            answer = answer[:amount]
        return answer

    @staticmethod
    def check_answer(this_try):
        answer = session['answer']
        i = 0
        correct_place = 0
        correct_color = 0
        guessed_colors = []

        for colors in this_try:
            if str(answer[i]) == str(colors):
                correct_place += 1
                i += 1
                continue
            if answer.__contains__(colors):
                if not guessed_colors.__contains__(colors):
                    correct_color -= -1
                guessed_colors.append(colors)
            i += 1
        return correct_color, correct_place

    @staticmethod
    def clear_game():
        if 'answer' in session:
            session.pop('answer')
        if 'amount' in session:
            session.pop('amount')
        if 'color_amount' in session:
            session.pop('color_amount')
        if 'game_id' in session:
            session.pop('game_id')
        if 'colors' in session:
            session.pop('colors')
        if 'tries' in session:
            session.pop('tries')
        if 'win' in session:
            session.pop('win')
        if 'lose' in session:
            session.pop('lose')
        if 'cheating' in session:
            session.pop('cheating')
        if 'attempts' in session:
            session.pop('attempts')


def random_color(colors: [], amount: int):
    answer = []
    for i in range(amount):
        answer.append(random.choice(colors))
    return answer
