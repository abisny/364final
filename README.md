# SI 364 - Winter 2018 - Final Project

**Final project submission deadline: April 20, 2018 at 11:59 pm**

**Total: 3200 points**

## Requirements to complete for 2880 points (90%) -- an awesome, solid app

### Installations
- Please install the IMDb Python API with the command `pip install imdbpy` in your terminal

### App Description
This app is an interactive movie database based on IMDb. Users can search for a movie to acquire information about it from both IMDb and Twitter (I used the IMDb and Twitter API's in addition to Beautiful Soup to scrape some of IMDb's actual website). IMDb supplies the year the movie in question was released and also a link to the movie searched on IMDb. If the user creates an account and/or logs in, they can play a game based on IMDb's top 250 movie list, which I have secured via the IMDb API. The user attempts to guess any/all of the 250 movies in question, and the game is then saved to their account. A user is only allowed to continue games they have created, though they can view the top scores, which includes a list of the top 10 scoring games out of all games (by any user).

### **How to Use**
A non-user can search for movies and receive information from IMDb, but cannot view search history or play a game. However, the non-user can view the top scores of all games by any user at the the `/top_scores` route.
Once logged in, a user can do two main exercises:
 (1) The user can search for movies and then view their search history, which will update with movies searched for on the `/movie_search` route and also on the `/play_game` route. A user can "clear" their search history (which deletes all `Movie` objects for which they have searched).
 (2) The user can create a new game or continue an old one via the `my_games` route, which is only viewable to a logged in user. The game allows the user to enter the title of a movie, and the user receives a point each time they guess a movie that is in IMDb's top 250 movies (which was retrieved via the API). A `Game` object can be deleted.

### **Routes**
- `'/'` -> `base.html`
- `'/login'` -> `login.html`
- `'/logout'` -> logs out `current_user` and redirects to `'/'`
- `'/register'` -> `register.html`
- `'/movie_search'` -> `movie_form.html`
- `'/search_history'` -> `search_history.html`
- `'/movie/<title>'` -> `movie_info.html`
- `'/delete_movies'` -> deletes all `Movie` objects and redirects to `'/movie_search'`
- `'/play_game/<game_id>'` -> `game.html` and `game_result.html`
- `'/new_game/<username>'` -> creates a new `Game` object and redirects to `'/play_game/<game_id>'`
- `'/delete/<game_id'` -> deletes `Game` object and redirects to `'/my_games'`
- `'/my_games'` -> `my_games.html`
- `'/display_game/<game_id>'` -> `game_info.html`
- `'/top_scores'` -> `top_scores.html`

### **Code Requirements**

- [x] **Ensure that your `SI364final.py` file has all the setup (`app.config` values, import statements, code to run the app if that file is run, etc) necessary to run the Flask application, and the application runs correctly on `http://localhost:5000` (and the other routes you set up). Your main file must be called `SI364final.py`, but of course you may include other files if you need.**

- [x] **A user should be able to load `http://localhost:5000` and see the first page they ought to see on the application.**

- [x] **Include navigation in `base.html` with links (using `a href` tags) that lead to every other page in the application that a user should be able to click on. (e.g. in the lecture examples from the Feb 9 lecture, [like this](https://www.dropbox.com/s/hjcls4cfdkqwy84/Screenshot%202018-02-15%2013.26.32.png?dl=0) )**

- [x] **Ensure that all templates in the application inherit (using template inheritance, with `extends`) from `base.html` and include at least one additional `block`.**

- [x] **Must use user authentication (which should be based on the code you were provided to do this e.g. in HW4).**

- [x] **Must have data associated with a user and at least 2 routes besides `logout` that can only be seen by logged-in users.**

- [x] **At least 3 model classes *besides* the `User` class.**

- [x] **At least one one:many relationship that works properly built between 2 models.**

- [x] **At least one many:many relationship that works properly built between 2 models.**

- [x] **Successfully save data to each table.**

- [x] **Successfully query data from each of your models (so query at least one column, or all data, from every database table you have a model for) and use it to effect in the application (e.g. won't count if you make a query that has no effect on what you see, what is saved, or anything that happens in the app).**

- [x] **At least one query of data using an `.all()` method and send the results of that query to a template.**

- [x] **At least one query of data using a `.filter_by(...` and show the results of that query directly (e.g. by sending the results to a template) or indirectly (e.g. using the results of the query to make a request to an API or save other data to a table).**

- [x] **At least one helper function that is *not* a `get_or_create` function should be defined and invoked in the application.**

- [ ] At least two `get_or_create` functions should be defined and invoked in the application (such that information can be saved without being duplicated / encountering errors).

- [x] **At least one error handler for a 404 error and a corresponding template.**

- [x] **At least one error handler for any other error (pick one -- 500? 403?) and a corresponding template.**

- [x] **Include at least 4 template `.html` files in addition to the error handling template files.**

  - [x] **At least one Jinja template for loop and at least two Jinja template conditionals should occur amongst the templates.**

- [x] **At least one request to a REST API that is based on data submitted in a WTForm OR data accessed in another way online (e.g. scraping with BeautifulSoup that *does* accord with other involved sites' Terms of Service, etc).**

  - [x] **Your application should use data from a REST API or other source such that the application processes the data in some way and saves some information that came from the source *to the database* (in some way).**

- [x] **At least one WTForm that sends data with a `GET` request to a *new* page.**

- [x] **At least one WTForm that sends data with a `POST` request to the *same* page. (NOT counting the login or registration forms provided for you in class.)**

- [x] **At least one WTForm that sends data with a `POST` request to a *new* page. (NOT counting the login or registration forms provided for you in class.)**

- [x] **At least two custom validators for a field in a WTForm, NOT counting the custom validators included in the log in/auth code.**

- [x] **Include at least one way to *update* items saved in the database in the application (like in HW5).
NOTE: THIS WAS DONE IN THAT YOU CAN 'CONTINUE' AN OLD GAME. I DO NOT EXPLICITLY USE THE WORD UPDATE, BUT THE BUTTON THAT SAYS CONTINUE CARRIES OUT THE 'UPDATE' CONCEPT, AS THE USER IS UPDATING THE LIST OF GUESSED MOVIES WHEN THEY CONTINUE A GAME.**

- [x] **Include at least one way to *delete* items saved in the database in the application (also like in HW5).**

- [x] **Include at least one use of `redirect`.**

- [x] **Include at least two uses of `url_for`. (HINT: Likely you'll need to use this several times, really.)**

- [x] **Have at least 5 view functions that are not included with the code we have provided. (But you may have more! *Make sure you include ALL view functions in the app in the documentation and navigation as instructed above.*)**


## Additional Requirements for additional points -- an app with extra functionality!

**Note:** Maximum possible % is 102%.

- [ ] (100 points) Include a use of an AJAX request in your application that accesses and displays useful (for use of your application) data.
- [x] **(100 points) Create, run, and commit at least one migration.**
- [ ] (100 points) Include file upload in your application and save/use the results of the file. (We did not explicitly learn this in class, but there is information available about it both online and in the Grinberg book.)
- [ ]  (100 points) Deploy the application to the internet (Heroku) — only counts if it is up when we grade / you can show proof it is up at a URL and tell us what the URL is in the README. (Heroku deployment as we taught you is 100% free so this will not cost anything.)
- [ ]  (100 points) Implement user sign-in with OAuth (from any other service), and include that you need a *specific-service* account in the README, in the same section as the list of modules that must be installed.
