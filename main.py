from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from apis import chucknorris

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

    def __str__(self):
        return f'Joke[id: {self.id}, value: {self.value}, comments count: {len(self.comments)}]'

    def __repr__(self):
        return str(self)


class Comment(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    value = db.Column(db.TEXT, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    joke_id = db.Column(db.TEXT, db.ForeignKey('joke.id'), nullable=False)
    created_at = db.Column(db.TEXT, default=str(datetime.now()), nullable=False)

    def __str__(self):
        return f'Comment[id: {self.id}, value: {self.value}]'

    def __repr__(self):
        return str(self)


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.TEXT, nullable=False)
    first_name = db.Column(db.TEXT)
    last_name = db.Column(db.TEXT)
    email = db.Column(db.TEXT)
    password = db.Column(db.TEXT, nullable=False)
    created_at = db.Column(db.TEXT, default=str(datetime.now()), nullable=False)
    comments = db.relationship('Comment', backref='author')

    def __str__(self):
        return f'User[id: {self.id}, username: {self.username}]'

    def __repr__(self):
        return str(self)


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


@app.route('/joke/<string:joke_id>')
def joke(joke_id):
    joke_obj = Joke.query.filter_by(id=joke_id).first()
    if joke_obj:
        return render_template('joke.html', joke=joke_obj)
    return 'error 404'


@app.route('/newjoke')
def newjoke():
    joke_json = chucknorris.get_random()
    if len(Joke.query.filter_by(id=joke_json['id']).all()) == 0:
        joke_obj = Joke(**joke_json)
        db.session.add(joke_obj)
        db.session.commit()

    return redirect(url_for('joke', joke_id=joke_json['id']))


if __name__ == '__main__':
    db.create_all()
    app.run(debug=True)
