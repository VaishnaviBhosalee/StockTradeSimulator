from flask import render_template,redirect
from create_app import app
from extensions import db

@app.route('/leaderboard')
def leaderboard():
    return render_template('leaderboard.html')