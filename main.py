from flask import Flask, render_template, request, redirect, url_for, session, flash, abort
from flask.views import MethodView
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from apis import chucknorris, spoonacular

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
    if 'user_id' in session:
        return redirect(url_for('profile', user_id=session['user_id']))

    if request.method == 'POST':
        username = request.form.get('username', '')
        password = request.form.get('password', '')

        if not username:
            flash('Input username', 'username_err')
        if not password:
            flash('Input password', 'password_err')
        if not (username and password):
            return render_template('login.html', username=username)

        user = User.query.filter_by(username=username).first()

        if not user:
            flash('Incorrect username', 'username_err')
            return redirect(url_for('login'))

        if user.password != password:
            flash('Incorrect password', 'password_err')
            return render_template('login.html', username=username)

        session['user_id'] = user.id
        return redirect(url_for('profile', user_id=user.id))

    return render_template('login.html')


@app.route('/logout')
def logout():
    session.pop('user_id', None)
    return redirect(url_for('login'))


@app.route('/signup', methods=['POST', 'GET'])
def registration():
    if 'user_id' in session:
        return redirect(url_for('profile'))

    if request.method == 'POST':
        return redirect(url_for('profile'))
    return render_template('registration.html')


class UserMethodView(MethodView):
    def get(self, user_id):
        if user_id is None:
            return redirect(url_for('login'))

        user = User.query.filter_by(id=user_id).first()
        if not user:
            abort(404)

        return render_template('profile.html', user=user, is_editable=user.id == session.get('user_id', ''))

    def post(self, user_id):
        if user_id != session.get('user_id', ''):
            return redirect(url_for('profile', user_id=user_id))

        user = User.query.filter_by(id=user_id).first()

        username, f_name, l_name, email = [request.form.get(key, '') for key in
                                           ['username', 'first_name', 'last_name', 'email']]
        old_pass, new_pass, conf_pass = [request.form.get(key, '') for key in
                                         ['old_password', 'new_password', 'conf_password']]
        if not username:
            flash('Input username', 'username_err')
        elif user.username != username and len(User.query.filter_by(username=username).all()) != 0:
            flash('Username already exists', 'username_err')
        else:
            user.username = username

        if f_name:
            user.first_name = f_name
        if l_name:
            user.last_name = l_name

        if email:
            if email.count('@') != 1 or email.split('@')[-1].count('.') != 1:
                flash('Incorrect email', 'email_err')
            else:
                user.email = email

        if old_pass or new_pass or conf_pass:
            if user.password != old_pass:
                flash('Incorrect password', 'old_pass_err')
            elif new_pass != conf_pass:
                flash('Passwords not match', 'conf_pass_err')
            elif not new_pass:
                flash('Input new password', 'new_pass_err')
            elif len(new_pass) < 8:
                flash('Password must be at least 8 characters long', 'new_pass_err')
            elif old_pass == new_pass:
                flash('This is old password', 'new_pass_err')
            else:
                user.password = new_pass

        db.session.commit()
        return redirect(url_for('profile', user_id=user_id))


app.add_url_rule('/profile/<int:user_id>', view_func=UserMethodView.as_view('profile'))


@app.route('/recipes')
def recipes():
    food_name = request.args.get('query', '')
    foods = spoonacular.get_receipts(food_name)
    return render_template('recipes.html', recipes=foods)


@app.route('/jokes')
def jokes():
    jokes_list = Joke.query.all()
    return render_template('jokes.html', jokes=jokes_list)


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
