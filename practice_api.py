# practice_api.py
# Abigail Snyder
# SI 364: HW 6
# April 11, 2018

# NOTE: this demonstrates my use of the IMDb API. I will also be scraping part of the IMDb
#       website using Beautiful Soup, as well as using the Twitter "Tweepy" API to get
#       additional data about the movies.

from imdb import IMDb # pip install imdbpy

# Game class model
class Game():
    def __init__(self, player_name=''):
        self.player_name = player_name
        self.current_score = 0
        self.guesses=[]
    def __repr__(self):
        return "\nGame by {}- Current Score: {}\n\tPrevious Guesses: {}".format(self.player_name, self.current_score, self.guesses)
    # IMDb api to get top 250 movies
    def guess_movie(self, guess):
        ia = IMDb()
        # top_250 data used to check whether or not the user guessed an accurate movie
        top_250 = [str(item) for item in ia.get_top250_movies()]
        if guess not in self.guesses and guess in top_250:
            self.current_score+=1
            print('Congrats! {} was in IMDb\'s top 250 movies list!'.format(guess))
        else: print('Sorry! {} was not in IMDb\'s top 250 movies list!'.format(guess))
        self.guesses.append(guess)

# main program creates a Game instance and guesses three movie titles
# the results are printed
game = Game(player_name='Abigail')
game.guess_movie('The Shawshank Redemption')
game.guess_movie('The Wizard of Oz')
game.guess_movie('Breakfast at Tiffany\'s')
print(game)
