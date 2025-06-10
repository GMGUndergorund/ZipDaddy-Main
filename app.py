from flask import Flask, render_template, request, redirect, url_for, session, abort
import os
import json

app = Flask(__name__)
app.secret_key = 'your_secret_key_here'  # Change to something strong and secret!

USERNAME = 'Zipdaddy'
PASSWORD = 'Kareem.1707'

def load_games():
    if os.path.exists('games.json'):
        with open('games.json', 'r') as f:
            return json.load(f)
    return []

def save_games(games):
    with open('games.json', 'w') as f:
        json.dump(games, f, indent=2)

@app.route('/')
def index():
    games = load_games()
    return render_template('index.html', games=games)

@app.route('/game/<int:game_id>')
def game_detail(game_id):
    games = load_games()
    if game_id < 0 or game_id >= len(games):
        abort(404)
    game = games[game_id]
    return render_template('game_detail.html', game=game)

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username'].strip()
        password = request.form['password'].strip()
        if username == USERNAME and password == PASSWORD:
            session['logged_in'] = True
            return redirect(url_for('upload'))
        else:
            return 'Invalid credentials'
    return render_template('login.html')

@app.route('/upload', methods=['GET', 'POST'])
def upload():
    if not session.get('logged_in'):
        return redirect(url_for('login'))

    if request.method == 'POST':
        title = request.form['title'].strip()
        download_link = request.form['download_link'].strip()
        description = request.form.get('description', '').strip()

        if not title or not download_link:
            return "Title and Download Link are required."

        if not (download_link.startswith('http://') or download_link.startswith('https://')):
            return "Download Link must be a valid URL starting with http:// or https://"

        games = load_games()
        games.append({
            'title': title,
            'download_link': download_link,
            'description': description
        })
        save_games(games)
        return redirect(url_for('index'))

    return render_template('upload.html')

@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
