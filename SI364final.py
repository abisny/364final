###############################
####### SETUP (OVERALL) #######
###############################

## Import statements
import os
from flask import Flask, render_template, session, redirect, url_for, flash, request
from bs4 import BeautifulSoup
import requests, re
from imdb import IMDb # pip install imdbpy

from flask_script import Manager, Shell

# Flask WTForms
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, RadioField, PasswordField, BooleanField # Note that you may need to import more here! Check out examples that do what you want to figure out what.
from wtforms.validators import Required, ValidationError, Length

# SQLAlchemy
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate, MigrateCommand

# Flask Login
from flask_login import LoginManager, login_required, logout_user, login_user, UserMixin, AnonymousUserMixin, current_user
from werkzeug.security import generate_password_hash, check_password_hash

basedir = os.path.abspath(os.path.dirname(__file__))

## App setup code
app = Flask(__name__)
app.debug = True
app.use_reloader = True

## All app.config values
app.config['SECRET_KEY'] = 'secretstring364final'
app.static_folder = 'static'
app.config['SQLALCHEMY_DATABASE_URI'] = "postgres://AbbySnyder@localhost/abisny364final"
app.config['SQLALCHEMY_COMMIT_ON_TEARDOWN'] = True
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

## Statements for db setup (and manager setup if using Manager)
manager = Manager(app)
db = SQLAlchemy(app) # For database use
migrate = Migrate(app, db) # For database use/updating
manager.add_command('db', MigrateCommand) # Add migrate command to manager

# Login configurations setup
login_manager = LoginManager()
login_manager.session_protection = 'strong'
login_manager.login_view = 'login'
login_manager.init_app(app) # set up login manager

## Set up Shell context so it's easy to use the shell to debug
def make_shell_context():
    return dict(app=app, db=db, User=User)
manager.add_command("shell", Shell(make_context=make_shell_context))


##################
##### MODELS #####
##################

class User(UserMixin, db.Model):
    __tablename__ = "users"
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(255), unique=True, index=True)
    password_hash = db.Column(db.String(128))
    games = db.relationship('Game', backref='User') # one-to-many relationship between a user and its games
    movies = db.relationship('Movie', secondary=search_history, backref=db.backref('movies', lazy='dynamic'), lazy='dynamic')
    @property
    def password(self):
        raise AttributeError('Password is not a readable attribute')
    @password.setter
    def password(self, password):
        self.password_hash = generate_password_hash(password)
    def verify_password(self, password):
        return check_password_hash(self.password_hash,  password)
## DB load function
@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id)) # returns User object or None

# ASSOCIATION TABLE: many-to-many relationship between games and movies
guessed_movies = db.Table('guessed_movies', db.Column('game_id', db.Integer, db.ForeignKey('games.id')),
                                            db.Column('movie_title', db.String, db.ForeignKey('movies.title')))

# ASSOCIATION TABLE: many-to-many relationship between users and movies
search_history = db.Table('search_history', db.Column('username', db.String, db.ForeignKey('users.username')),
                                            db.Column('movie_title', db.String, db.ForeignKey('movies.title')))
# TODO: run a migration so that this association table will generate and the code will run

class Movie(db.Model):
    __tablename__ = "movies"
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(64), unique=True)
    release_year = db.Column(db.Integer,  db.ForeignKey('years.name'))
    rank = db.Column(db.Integer)
    def __repr__(self):
        return "{}, {} (ID: {})".format(self.title, self.release_year, self.id)

class Year(db.Model):
    __tablename__ = "years"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.Integer, unique=True)
    movies = db.relationship('Movie', backref='Year')   # one-to-many relationship between a year and its movies
    def __repr__(self):
        return "{} (ID: {})".format(self.name, self.id)

class Game(db.Model):
    __tablename__ = "games"
    id = db.Column(db.Integer, primary_key=True)
    player = db.Column(db.String(64), db.ForeignKey('users.username'))
    current_score = db.Column(db.Integer)
    guesses = db.relationship('Movie', secondary=guessed_movies, backref=db.backref('movies', lazy='dynamic'), lazy='dynamic')
    def __repr__(self):
        return "Game #{} ({}): {}".format(self.id, self.player, self.current_score)


###################
###### FORMS ######
###################

class LoginForm(FlaskForm):
    username = StringField("Username.", validators=[Required()])
    password = PasswordField('Password', validators=[Required()])
    submit = SubmitField('Log In')

class RegistrationForm(FlaskForm):
    username = StringField('Username:', validators=[Required(), Length(1,64)])
    password = PasswordField('Password:', validators=[Required(), Length(6,64)])
    submit = SubmitField('Register')
    def validate_username(self,field):
        if User.query.filter_by(username=field.data).first():
            raise ValidationError('Sorry. That username is already taken.')

class MovieForm(FlaskForm):
    title = StringField("Search for a movie by title.", validators=[Required()])
    submit = SubmitField()
    def validate_title(self, field):
        ia = IMDb()
        r = requests.get('http://www.imdb.com/find?q=' + field.data + '&s=all')
        soup = BeautifulSoup(r.content, 'html.parser')
        results = soup.find_all('td',{'class':'result_text'})
        titles = [item.a.contents[0] for item in results]
        if titles[0] != field.data:
            raise ValidationError("The title you entered was not found in the IMDb database. Check spelling and try again.")

class GameForm(FlaskForm):
    guess = StringField("Guess a top 250 movie title here.", validators=[Required()])
    submit = SubmitField()
    def validate_guess(self, field):
        ia = IMDb()
        r = requests.get('http://www.imdb.com/find?q=' + field.data + '&s=all')
        soup = BeautifulSoup(r.content, 'html.parser')
        results = soup.find_all('td',{'class':'result_text'})
        titles = [item.a.contents[0] for item in results]
        if titles[0] != field.data:
            raise ValidationError("The title you entered was not found in the IMDb database. Check spelling and try again.")


######################################
############ HELPER FXNS #############
######################################

# MODIFIES: db table movies
# EFFECTS: scrapes IMDb page to get release_year of searched movie and adds movie and
#          corresponding year to database; returns movie
def imdb_get_movie(title, rank=None):
    r = requests.get('http://www.imdb.com/find?q=' + title + '&s=all')
    soup = BeautifulSoup(r.content, 'html.parser')
    results = soup.find_all('td', {'class':'result_text'})
    regex = [re.search('[0-9]+', result.contents[2]) for result in results[:1]][0]
    for result in results[:1]: year = int(result.contents[2][regex.span()[0]:regex.span()[1]])
    titles = [item.a.contents[0] for item in results]
    movie = Movie.query.filter_by(title=titles[0], release_year=year).first()
    if movie:
        movie.rank = rank
        return movie
    return create_movie_and_year(title=titles[0], release_year=year, rank=rank)

# REQUIRES: title is a string, release_year is an int
# MODIFIES: db tables movies, years
# EFFECTS: adds release_year to Years if not there, adds movie to Movies if
#          not there (with foreign key release_year)
def create_movie_and_year(title, release_year, rank=None):
    if not Year.query.filter_by(name=release_year).first():
        db.session.add(Year(name=release_year))
    movie = Movie(title=title, release_year=release_year, rank=rank)
    if (current_user.is_authenticated):
        User.query.filter_by(id=current_user.id).first().movies.append(movie)
    db.session.add(movie)
    db.session.commit()
    return movie


# REQUIRES: valid game_id, guess is a string
# MODIFIES: row for given game_id in table games
# EFFECTS: increments score for game at game_id by one and adds the guess to the
#          "list" of guesses attached to game (all if guess hasn't already been made)
def increment_score(game, guess, movie):
    if guess not in game.guesses:
        game.current_score += 1
        game.guesses.append(movie)
        db.session.commit()
        return False
    return True


#######################
###### VIEW FXNS ######
#######################

## Error handling routes ##
@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404

@app.errorhandler(500)
def internal_server_error(e):
    return render_template('500.html'), 500
###########################

@app.route('/', methods=['GET', 'POST'])
def home():
    return render_template('base.html', logged_in=current_user.is_authenticated)

@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user is not None and user.verify_password(form.password.data):
            login_user(user)
            return redirect(url_for('home'))
        flash('Invalid username or password.')
    return render_template('login.html', form=form, logged_in=current_user.is_authenticated)

@app.route('/logout')
@login_required
def logout():
    logout_user()
    flash('You are now logged out.')
    return redirect(url_for('home'))

@app.route('/register', methods=['GET', 'POST'])
def register():
    form = RegistrationForm()
    if form.validate_on_submit():
        user = User(username=form.username.data, password=form.password.data)
        db.session.add(user)
        db.session.commit()
        return redirect(url_for('login'))
    return render_template('register.html', form=form, logged_in=current_user.is_authenticated)

@app.route('/movie_search', methods=['GET', 'POST'])
def movie_search():
    form = MovieForm()
    if form.validate_on_submit():
        movie = imdb_get_movie(title=form.title.data)
        twitter_data = requests.get('https://api.twitter.com/1.1/search/tweets.json?q={}&count=5'.format(form.title.data)).text
        # TODO: get appropriate Twitter data to display in '/movie/<title>' route
        return redirect(url_for('display_movie', title=movie.title))
    elif 'title' in form.errors: flash(form.errors['title'][0])
    return render_template('movie_form.html', form=form, logged_in=current_user.is_authenticated)

@app.route('/all_movies', methods=['GET', 'POST'])
def all_movies():
    if current_user.is_authenticated:
        movies = User.query.filter_by(current_user.id).first().movies
    else: movies = []
    return render_template('all_movies.html', movies=movies, logged_in=current_user.is_authenticated)

@app.route('/movie/<title>', methods=['GET', 'POST'])
def display_movie(title):
    movie = Movie.query.filter_by(title=title).first()
    return render_template('movie_info.html', movie=movie, logged_in=current_user.is_authenticated)

@app.route('/delete_movies', methods=['GET', 'POST'])
def delete_movies():
    for movie in Movie.query.all():
        db.session.delete(movie)
    db.session.commit()
    flash('No search history to be shown.')
    return redirect(url_for('movie_search'))

@app.route('/play_game/<game_id>', methods=['GET', 'POST'])
@login_required
def play_game(game_id):
    game_form = GameForm()
    game = Game.query.filter_by(id=game_id).first()
    if game_form.validate_on_submit():
        ia = IMDb()
        top_250 = [str(title) for title in ia.get_top250_movies()]
        rank = None
        already_guessed = False
        for i in range(0, 250):
            if (game_form.guess.data == top_250[i]): rank = i + 1
        if rank:
            movie = imdb_get_movie(title=game_form.guess.data, rank=rank)
            already_guessed = increment_score(game=game, guess=game_form.guess.data, movie=movie)
        db.session.commit()
        return render_template('game_result.html', game=game, guesses=game.guesses, to_go=250-len(guesses), rank=rank, already_guessed=already_guessed, logged_in=current_user.is_authenticated)
    return render_template('game.html', form=game_form, logged_in=current_user.is_authenticated)

@app.route('/delete/<game_id>', methods=['GET', 'POST'])
@login_required
def delete(game_id):
    db.session.delete(Game.query.filter_by(id=game_id).first())
    db.session.commit()
    flash('Game #{} has been permenantly deleted'.format(game_id))
    return redirect(url_for('view_my_scores'))

@app.route('/my_games', methods=['GET', 'POST'])
@login_required
def view_my_scores():
    username = User.query.filter_by(id=current_user.id).first().username
    games = Game.query.filter_by(player=username).all()
    new_game = None
    # TODO: fix new_game; it is currently setting ID to None
    if not games: new_game = Game(player=username, current_score=0)
    return render_template('my_games.html', games=games, new_game=new_game, logged_in=current_user.is_authenticated)

@app.route('/display_game/<game_id>', methods=['GET', 'POST'])
@login_required
def display_game(game_id):
    game = Game.query.filter_by(id=game_id).first()
    return render_template('game_info.html', game=game, guesses=game.guesses, to_go=250-len(guesses), logged_in=current_user.is_authenticated)

@app.route('/top_scores', methods=['GET', 'POST'])
def view_scores():
    def current_score(game):
        return game.current_score
    sorted_games = sorted(Game.query.all(), key=current_score, reverse=True)[:10]
    return render_template('top_scores.html', sorted_games=sorted_games, logged_in=current_user.is_authenticated)


## Code to run the application...
if __name__ == '__main__':
    db.create_all() # Will create any defined models when you run the application
    app.run(use_reloader=True,debug=True) # The usual
