from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

app = Flask(__name__)
app.secret_key = 'text'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///db.sqlite3'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)


class Joke(db.Model):
    id = db.Column(db.TEXT, primary_key=True)
    value = db.Column(db.TEXT, nullable=False)
    url = db.Column(db.TEXT, nullable=False)
    icon_url = db.Column(db.TEXT, nullable=False)
    updated_at = db.Column(db.TEXT, nullable=False)
    created_at = db.Column(db.TEXT, nullable=False)
    comments = db.relationship('Comment', backref='joke')


class Comment(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    value = db.Column(db.TEXT, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    joke_id = db.Column(db.TEXT, db.ForeignKey('joke.id'), nullable=False)
    created_at = db.Column(db.TEXT, default=str(datetime.now()), nullable=False)


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.TEXT, nullable=False)
    first_name = db.Column(db.TEXT)
    last_name = db.Column(db.TEXT)
    email = db.Column(db.TEXT)
    password = db.Column(db.TEXT, nullable=False)
    created_at = db.Column(db.TEXT, default=str(datetime.now()), nullable=False)
    comments = db.relationship('Comment', backref='author')


@app.route('/')
def index():
    return render_template('home.html')


@app.route('/login', methods=['POST', 'GET'])
def login():
    if request.method == 'POST':
        return redirect(url_for('profile'))

    return render_template('login.html')


@app.route('/logout')
def logout():
    return render_template('logout.html')


@app.route('/signup', methods=['POST', 'GET'])
def registration():
    if request.method == 'POST':
        return redirect(url_for('profile'))
    return render_template('registration.html')


@app.route('/profile')
def profile():
    return render_template('profile.html')


@app.route('/receipts')
def receipts():
    return redirect(url_for())


if __name__ == '__main__':
    db.create_all()
    app.run(debug=True)
