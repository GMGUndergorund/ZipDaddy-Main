# init_db.py
from flask import Flask
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///games.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

class Game(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    download_link = db.Column(db.String(300), nullable=False)
    description = db.Column(db.Text, nullable=True)
    genres = db.Column(db.String(200), nullable=True)

with app.app_context():
    db.create_all()
    print("✅ games.db wurde erstellt!")
