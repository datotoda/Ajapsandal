from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy

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


class Comment(db.Model):
    id = db.Column(db.INT, primary_key=True)
    value = db.Column(db.TEXT, nullable=False)
    author = db.Column(db.TEXT, nullable=False)
    joke = db.Column(db.TEXT, nullable=False)
    created_at = db.Column(db.TEXT, nullable=False)


class User(db.Model):
    id = db.Column(db.INT, primary_key=True)
    username = db.Column(db.TEXT, nullable=False)
    first_name = db.Column(db.TEXT, nullable=False)
    last_name = db.Column(db.TEXT, nullable=False)
    email = db.Column(db.TEXT, nullable=False)
    password = db.Column(db.TEXT, nullable=False)
    created_at = db.Column(db.TEXT, nullable=False)


@app.route('/')
def index():
    return render_template('home.html')


if __name__ == '__main__':
    app.run(debug=True)


@app.route('/login', methods=['POST', 'GET'])
def login():
    if request.method == 'POST':
        # user = request.
        # session['user'] = user
        return redirect(url_for('profile'))

    return render_template('login.html')


@app.route('/logout')
def logout():
    pass
