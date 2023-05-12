from flask import Flask, render_template, redirect, url_for, request, flash
from flask_bootstrap import Bootstrap
from forms import RateMovieForm, FindMovieForm
from config import init_app, db, create_app
from sqlalchemy.exc import SQLAlchemyError
from dotenv import load_dotenv
from models import Movies
import requests
import os

# Initialize Flask, Bootstrap and DB.
app = Flask(__name__)
Bootstrap(app)
init_app(app)
create_app(app)

# Sets the API endpoint.
MOVIE_DB_SEARCH_URL = "https://api.themoviedb.org/3/search/movie?"

# Load .env variables and get rid of the quotes in them.
load_dotenv("E:/Python/EnvironmentVariables/.env")
app.config['SECRET_KEY'] = os.getenv("APP_SECRET_KEY").replace('"', '')
TMDB_API_KEY = os.getenv("TMDB_API_KEY").replace('"', '')

# Sets the desired movies list length.
LIST_LEN = 10

@app.route("/")
def home():
    # Order the movies by descending order.
    movies = db.session.query(Movies).order_by(Movies.rating.desc()).all()

    # Loop through the movies and assign them the "ranking" by their place.
    num_movies = len(movies)
    for i, movie in enumerate(movies):
        movie.ranking = num_movies - i
        db.session.add(movie)
    db.session.commit()  # Commit the changes to the db.
    return render_template("index.html", movies=movies, len=len(movies))


@app.route('/add', methods=['GET', 'POST'])
def fetch_movies_list():
    """
    Function finds movie list by movie title.
    :return: List of the movies, if found.
    """
    if db.session.query(Movies).count() >= LIST_LEN:  # Check if reached maximum movies.
        flash("You have reached the maximum number of movies in the list.\nDelete a movie to add another one.", 'warning')
    else:
        form = FindMovieForm()
        if form.validate_on_submit():
            movie_title = form.title.data  # Get the movies list that match the search.
            # Makes an API call.
            response = requests.get(f"{MOVIE_DB_SEARCH_URL}", params={"api_key": TMDB_API_KEY, "query": movie_title})
            data = response.json()["results"]
            if response.status_code == 200 and data:  # Checks if the API call and json fetching was successful.
                return render_template("select.html", movies=data)
            else:
                print(f"FAIL! \n{response.text}")
                return redirect(url_for('home'))
        return render_template("add.html", form=form)
    return redirect(url_for('home'))


@app.route('/rate_movie', methods=["GET", "POST"])
def rate_movie():
    """
    Function handles the 'edit' button for each movie.
    """
    form = RateMovieForm()  # Create new form.
    movie_id = request.args.get('id')  # Get the wanted movie to edit.
    movie_to_update = db.session.get(Movies, movie_id)
    if movie_to_update is not None:  # If the movie was found.
        if form.validate_on_submit():  # Check if the form was sent successfully.
            # Try to edit the db to the new data.
            try:
                movie_to_update.rating = request.form['rating']
                movie_to_update.review = request.form['review']
                db.session.commit()
            except SQLAlchemyError as e:
                db.session.rollback()
                flash(f'An error occurred while updating the movie.\n{e}')
            finally:
                return redirect(url_for('home'))  # Redirect the user to homepage.
    else:  # Movie was not found
        return redirect(url_for('home'))  # Redirect the user to homepage.
    return render_template('rate_movie.html', form=form, movie=movie_to_update)


@app.route('/delete')
def delete():
    """
    Function handles the deletion of a movie.
    :return: Home page after deletion.
    """
    with app.app_context():
        movie_id = request.args.get('id')
        movie_to_delete = db.session.query(Movies).get(movie_id)
        db.session.delete(movie_to_delete)
        db.session.commit()
    return redirect(url_for('home'))


@app.route('/find')
def add_movie():
    """
    Function handles selection for particular movie in movies list.
    When the user clicks the desired movie, it will search the movie by ID
    and will add it to the DB with the title, img_url, year, description.
    :return: Redirect to homepage.
    """
    movie_api_id = request.args.get('id')
    if movie_api_id:  # Check if a movie id was entered.
        response = requests.get(
            f'https://api.themoviedb.org/3/movie/{movie_api_id}?api_key={TMDB_API_KEY}')
        if response.status_code == 200:  # Check if there are results to the API call.
            # Try to add the data to the db.
            try:
                movie_data = response.json()
                movie = Movies(
                    title=movie_data['title'],
                    year=movie_data['release_date'].split("-")[0],  # Get only the year.
                    description=movie_data['overview'],
                    rating=0,
                    ranking=0,
                    review=0,
                    img_url=f"https://image.tmdb.org/t/p/original{movie_data['poster_path']}"
                )
                db.session.add(movie)
                db.session.commit()
                return redirect(url_for('rate_movie', id=movie.id))
            except Exception as e:
                db.session.rollback()
    return redirect(url_for('home'))

@app.route('/details', methods=["GET", "POST"])
def movie_details():
    # Get the movie ID
    movie_id = request.args.get('id')
    movie_to_show = db.session.get(Movies, movie_id)
    if movie_to_show is not None:  # Check if succeeded pulling the movie.
        return render_template('movie_details.html', movie=movie_to_show) # Render the page...
    return redirect(url_for('home'))



if __name__ == '__main__':
    app.run(debug=True)
