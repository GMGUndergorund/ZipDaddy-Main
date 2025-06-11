from flask import Flask, render_template, request, redirect, url_for, session, abort
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.secret_key = 'your_secret_key_here'

# SQLite configuration
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///games.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

USERNAME = 'Zipdaddy'
PASSWORD = 'Kareem.1707'

class Game(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    download_link = db.Column(db.String(300), nullable=False)
    description = db.Column(db.Text, nullable=True)

@app.before_request
def create_tables_once():
    if not hasattr(app, 'tables_created'):
        db.create_all()
        app.tables_created = True

@app.route('/')
def index():
    search = request.args.get('search', '').strip()
    if search:
        games = Game.query.filter(Game.title.ilike(f'%{search}%')).order_by(Game.title.asc()).all()
    else:
        games = Game.query.order_by(Game.title.asc()).all()
    return render_template('index.html', games=games, search=search)

@app.route('/game/<int:game_id>')
def game_detail(game_id):
    game = Game.query.get_or_404(game_id)
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
            return 'Invalid credentials', 401
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
            return "Title and Download Link are required.", 400

        if not (download_link.startswith('http://') or download_link.startswith('https://')):
            return "Download Link must start with http:// or https://", 400

        # Optional: Check if game with same title exists, update or reject
        existing = Game.query.filter_by(title=title).first()
        if existing:
            return "A game with this title already exists.", 400

        new_game = Game(title=title, download_link=download_link, description=description)
        db.session.add(new_game)
        db.session.commit()

        return redirect(url_for('index'))

    return render_template('upload.html')

@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
