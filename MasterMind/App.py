import logging
import os

from flask import Flask, render_template, url_for, session, request

from Colors import Color
from Game import Game
from Player import Player
from db_connection import db_connection

app = Flask(__name__)
app.secret_key = os.urandom(24)
app.logger.setLevel(logging.INFO)

@app.route('/')
def home():
    return render_template('login.html')

@app.route('/login/', methods=['GET', 'POST'])
def login():
    if 'player' in session:
        return render_template('gamestart.html')
    if request.method == 'POST':
        username = request.form['user']
        if username == "":
            return render_template('login.html')
        else:
            Player(username)
            return render_template('gamestart.html')
    return render_template('login.html')


@app.route('/logout/')
def logout():
    if 'player' in session:
        session.clear()
    return render_template('login.html')


@app.route('/gamestart/', methods=['GET', 'POST'])
def gamestart():
    if request.method == 'GET' and 'player' in session:
        return render_template('gamestart.html')
    if request.method == 'POST' and 'player' in session:
        Game.clear_game()
        Player.begin_game()
        is_checked = request.form.get('doubles')
        cheat_on = request.form.get('cheat')
        session['answer'] = Game.generate_game(int(request.form['amount']), int(request.form['color_amount']), is_checked)
        session['is_cheated'] = False
        if cheat_on:
            session['is_cheated'] = True
            db_connection.query("UPDATE Game SET has_cheated = (?)" +
                                "WHERE game_id = (?)", (True, session['game_id']))
        if 'tries' not in session:
            session['tries'] = []
        return render_template('game.html', Color=Color, cheating=session['is_cheated'])
    return render_template('login.html')

@app.route('/game/', methods=['GET', 'POST'])
def game():
    if 'player' in session and 'game_id' in session:
        if 'tries' not in session:
            session['tries'] = []
        if request.method == 'POST':
            if 'attempts' in session:
                session['attempts'] += 1
            else:
                session['attempts'] = 1
            this_try = []
            for i in range(session['amount']):
                this_try.append(request.form[str(i)])
            this_try_correct = Game.check_answer(this_try)
            session['tries'].append([this_try, this_try_correct])
            if str(this_try_correct[1]) == str(session['amount']):
                session['win'] = True
                return render_template('game.html', Color=Color, win=True)
            if str(session['attempts']) == "10":
                session['lose'] = True
                return render_template('game.html', Color=Color, win=False, lose=True)
            return render_template('game.html', Color=Color, cheating=session['is_cheated'])
        return render_template('game.html', Color=Color, cheating=session['is_cheated'])
    return render_template('login.html')

@app.route('/win/', methods=['POST'])
def win():
    if 'player' in session and 'game_id' in session:
        if 'win' in session:
            if session['win'] is True:
                db_connection.query("UPDATE Game SET turns = (?)," +
                                    "is_finished = (?)" +
                                    "WHERE game_id = (?)", (session['attempts'], True, session['game_id']))
                Game.clear_game()
                return render_template('gamestart.html')
    session.clear()
    return render_template('login.html')

@app.route('/lose/', methods=['POST'])
def lose():
    if 'player' in session and 'game_id' in session:
        if 'lose' in session:
            if session['lose'] is True:
                db_connection.query("UPDATE Game SET turns = (?)," +
                                    "is_finished = (?)" +
                                    "WHERE game_id = (?)", (session['attempts'], False, session['game_id']))
                Game.clear_game()
                return render_template('gamestart.html')
    session.clear()
    return render_template('login.html')

@app.route('/statistics/')
def stats():
    if 'player' in session:
        d1 = db_connection.select_query('SELECT AVG(turns) FROM Game WHERE player_id = ? AND is_finished = true', [session['player_id']])[0][0]
        d2 = db_connection.select_query('SELECT COUNT(player_id) FROM Game WHERE player_id = ? AND is_finished = true', [session['player_id']])[0][0]
        d3 = db_connection.select_query('SELECT COUNT(*) - (SELECT COUNT(player_id) FROM Game WHERE player_id = ? '
                                        'AND is_finished = true) FROM Game WHERE player_id = ?', [session['player_id'], session['player_id']])[0][0]
        d4 = db_connection.select_query('SELECT created_at FROM Game WHERE player_id = ? order by '
                                        'created_at DESC LIMIT 1', [session['player_id']])[0][0]
        d5 = db_connection.select_query('SELECT COUNT(*) - (SELECT COUNT(player_id) FROM Game WHERE player_id = ? '
                                        'AND has_cheated = false) FROM Game WHERE player_id = ?', [session['player_id'], session['player_id']])[0][0]
        return render_template('statistics.html', db_connection=db_connection, d1=d1, d2=d2, d3=d3, d4=d4, d5=d5)
    return render_template('login.html')

if __name__ == '__main__':
    app.run()