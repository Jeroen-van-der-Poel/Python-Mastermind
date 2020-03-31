import logging
import os

from flask import Flask, render_template, url_for, session, request, redirect
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
        return render_template('game.html')
    if request.method == 'POST':
        username = request.form['user']
        Player(username)
        return redirect(url_for('game'))
    return render_template('login.html')

if __name__ == '__main__':
    app.run()