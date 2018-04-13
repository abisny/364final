# SI 364 - Winter 2018 - Final Project

**Final project submission deadline: April 20, 2018 at 11:59 pm**

**Total: 3200 points**

## Requirements to complete for 2880 points (90%) -- an awesome, solid app

### Installations
- Please install the IMDb Python API with the command `pip install imdbpy` in your terminal

### App Description
This app is an interactive movie database based on IMDb. Users can search for a movie to acquire information about it from both IMDb and Twitter (I used the IMDb and Twitter API's in addition to Beautiful Soup to scrape some of IMDb's actual website). IMDb supplies the year the movie in question was released, and the Twitter API supplies tweets regarding that film, to include a "popular" review of the movie. If the user creates an account and/or logs in, they can play a game based on IMDb's top 250 movie list, which I have secured via the IMDb API. The user attempts to guess any/all of the 250 movies in question, and the game is then saved to their account. A user is only allowed to continue games they have created, though they can view the top scores, which includes a list of the top 10 scoring games out of all games (by any user).

### **Documentation README Requirements**

- **[ ] Create a `README.md` file for your app that includes the full list of requirements from this page. The ones you have completed should be bolded or checked off. (You bold things in Markdown by using two asterisks, like this: `This text would be bold and this text would not be`)**

- **[ ] The `README.md` file should use markdown formatting and be clear / easy to read.**

- [ ] The `README.md` file should include a 1-paragraph (brief OK) description of what your application does

- [ ] The `README.md` file should include a detailed explanation of how a user can user the running application (e.g. log in and see what, be able to save what, enter what, search for what... Give us examples of data to enter if it's not obviously stated in the app UI!)

- [ ] The `README.md` file should include a list of every module that must be installed with `pip` if it's something you installed that we didn't use in a class session. If there are none, you should note that there are no additional modules to install.

- [ ] The `README.md` file should include a list of all of the routes that exist in the app and the names of the templates each one should render OR, if a route does not render a template, what it returns (e.g. `/form` -> `form.html`, like [the list we provided in the instructions for HW2](https://www.dropbox.com/s/3a83ykoz79tqn8r/Screenshot%202018-02-15%2013.27.52.png?dl=0) and like you had to on the midterm, or `/delete -> deletes a song and redirects to index page`, etc).

### **Code Requirements**

- **[o] Ensure that your `SI364final.py` file has all the setup (`app.config` values, import statements, code to run the app if that file is run, etc) necessary to run the Flask application, and the application runs correctly on `http://localhost:5000` (and the other routes you set up). **Your main file must be called `SI364final.py`, but of course you may include other files if you need.**

- **[o] A user should be able to load `http://localhost:5000` and see the first page they ought to see on the application.**

- **[ ] Include navigation in `base.html` with links (using `a href` tags) that lead to every other page in the application that a user should be able to click on. (e.g. in the lecture examples from the Feb 9 lecture, [like this](https://www.dropbox.com/s/hjcls4cfdkqwy84/Screenshot%202018-02-15%2013.26.32.png?dl=0) )**

- **[ ] Ensure that all templates in the application inherit (using template inheritance, with `extends`) from `base.html` and include at least one additional `block`.**

- **[ ] Must use user authentication (which should be based on the code you were provided to do this e.g. in HW4).**

- [ ] Must have data associated with a user and at least 2 routes besides `logout` that can only be seen by logged-in users.

- **[ ] At least 3 model classes *besides* the `User` class.**

- [ ] At least one one:many relationship that works properly built between 2 models.

- [ ] At least one many:many relationship that works properly built between 2 models.

- **[ ] Successfully save data to each table.**

- **[ ] Successfully query data from each of your models (so query at least one column, or all data, from every database table you have a model for) and use it to effect in the application (e.g. won't count if you make a query that has no effect on what you see, what is saved, or anything that happens in the app).**

- **[ ] At least one query of data using an `.all()` method and send the results of that query to a template.**

- **[ ] At least one query of data using a `.filter_by(...` and show the results of that query directly (e.g. by sending the results to a template) or indirectly (e.g. using the results of the query to make a request to an API or save other data to a table).**

- **[ ] At least one helper function that is *not* a `get_or_create` function should be defined and invoked in the application.**

- **[ ] At least two `get_or_create` functions should be defined and invoked in the application (such that information can be saved without being duplicated / encountering errors).**

- **[ ] At least one error handler for a 404 error and a corresponding template.**

- **[ ] At least one error handler for any other error (pick one -- 500? 403?) and a corresponding template.**

- **[ ] Include at least 4 template `.html` files in addition to the error handling template files.**

  - **[ ] At least one Jinja template for loop and at least two Jinja template conditionals should occur amongst the templates.**

- **[ ] At least one request to a REST API that is based on data submitted in a WTForm OR data accessed in another way online (e.g. scraping with BeautifulSoup that *does* accord with other involved sites' Terms of Service, etc).**

  - **[ ] Your application should use data from a REST API or other source such that the application processes the data in some way and saves some information that came from the source *to the database* (in some way).**

- **[ ] At least one WTForm that sends data with a `GET` request to a *new* page.**

- **[ ] At least one WTForm that sends data with a `POST` request to the *same* page. (NOT counting the login or registration forms provided for you in class.)**

- **[ ] At least one WTForm that sends data with a `POST` request to a *new* page. (NOT counting the login or registration forms provided for you in class.)**

- **[ ] At least two custom validators for a field in a WTForm, NOT counting the custom validators included in the log in/auth code.**

- **[ ] Include at least one way to *update* items saved in the database in the application (like in HW5).**

- **[ ] Include at least one way to *delete* items saved in the database in the application (also like in HW5).**

- **[ ] Include at least one use of `redirect`.**

- **[ ] Include at least two uses of `url_for`. (HINT: Likely you'll need to use this several times, really.)**

- **[ ] Have at least 5 view functions that are not included with the code we have provided. (But you may have more! *Make sure you include ALL view functions in the app in the documentation and navigation as instructed above.*)**


## Additional Requirements for additional points -- an app with extra functionality!

**Note:** Maximum possible % is 102%.

- [ ] (100 points) Include a use of an AJAX request in your application that accesses and displays useful (for use of your application) data.
- [ ]  (100 points) Create, run, and commit at least one migration.
- [ ] (100 points) Include file upload in your application and save/use the results of the file. (We did not explicitly learn this in class, but there is information available about it both online and in the Grinberg book.)
- [ ]  (100 points) Deploy the application to the internet (Heroku) — only counts if it is up when we grade / you can show proof it is up at a URL and tell us what the URL is in the README. (Heroku deployment as we taught you is 100% free so this will not cost anything.)
- [ ]  (100 points) Implement user sign-in with OAuth (from any other service), and include that you need a *specific-service* account in the README, in the same section as the list of modules that must be installed.


## **To submit**
- Commit all changes to your git repository. Should include at least the files:
  - `README.md`
  - `SI364final.py`
  - A `templates/` directory with all templates you have created inside it
  - May include others (e.g. may include a `static` folder if you are including or uploading static files, but this is not necessary!)
- Create a GitHub account called `364final` on your GitHub account. (You are NOT forking and cloning anything this time, you are creating your own repo from start to finish.)
  - Invite users `aerenchyma` (Jackie), `pandeymauli` (Mauli) and `Watel` (Sonakshi, or `sonakshi@umich.edu`) as collaborators on the repository. [Here's the reminder of how to add a collaborator to a repository](https://www.dropbox.com/s/d6btsfxgh6z84bx/Screenshot%202018-02-13%2021.32.11.png?dl=0).
- Submit the *link* to your GitHub repository to the **SI 364 Final Project** assignment on our Canvas site. The link should be of the form: `https://github.com/YOURGITHUBUSERNAME/364final` (if it doesn't look like that, you are probably linking to something specific *inside* the repo, so make sure it does look like that).

All set!
