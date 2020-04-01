import logging
import os

from flask import Flask, render_template, url_for, session, request, redirect

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
        Player(username)
        return render_template('gamestart.html')
    return render_template('login.html')


@app.route('/logout/')
def logout():
    if 'player' in session:
        session.clear()
    return render_template('login.html')


@app.route('/gamestart/', methods=['GET', 'POST'])
def game():
    if request.method == 'GET' and 'player' in session:
        return render_template('gamestart.html')
    if request.method == 'POST' and 'player' in session:
        Game.clear_game()
        Player.begin_game()
        is_checked = request.form.get('doubles')
        session['answer'] = Game.generate_game(int(request.form['amount']), int(request.form['color_amount']), is_checked)
        if 'tries' not in session:
            session['tries'] = []
        return render_template('game.html', Color=Color)
    return render_template('login.html')

@app.route('/statistics/')
def stats():
    if 'player' in session:
        d1 = db_connection.select_query('SELECT AVG(turns) FROM Game WHERE player_id = ? AND is_finished = true', [session['player_id']])[0][0]
        d2 = db_connection.select_query('SELECT COUNT(player_id) FROM Game WHERE player_id = ? AND is_finished = true', [session['player_id']])[0][0]
        d3 = db_connection.select_query('SELECT COUNT(*) - (SELECT COUNT(player_id) FROM Game WHERE player_id = ? '
                                        'AND is_finished = true) FROM Game WHERE player_id = ?', [session['player_id'], session['player_id']])[0][0]
        d4 = db_connection.select_query('SELECT created_at FROM Game WHERE player_id = ? order by '
                                        'created_at LIMIT 1', [session['player_id']])[0][0]
        return render_template('statistics.html', db_connection=db_connection, d1=d1, d2=d2, d3=d3, d4=d4)
    return render_template('login.html')


if __name__ == '__main__':
    app.run()