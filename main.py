from flask import Flask, render_template, redirect, url_for, request
from flask_bootstrap import Bootstrap
from forms import RateMovieForm, FindMovieForm
from config import init_app, db, create_app
from models import Movies
import requests

app = Flask(__name__)
app.config['SECRET_KEY'] = '8BYkEfBA6O6donzWlSihBXox7C0sKR6b'
Bootstrap(app)
init_app(app)

# Configure the "The Movie Database" API key.
TMDB_API_KEY = "4a28abb8e4029298f9d249e2c8944907"
MOVIE_DB_SEARCH_URL = "https://api.themoviedb.org/3/search/movie?"

create_app(app)


@app.route("/")
def home():
    # Order the movies by their rating with descending order
    movies = db.session.query(Movies).order_by(Movies.rating.desc()).all()

    # Loop through the movies and assign them the "ranking" by their place.
    for i, movie in enumerate(movies):
        movie.ranking = 10 - i
        db.session.add(movie)
    db.session.commit()
    return render_template("index.html", movies=movies)


@app.route('/rate_movie', methods=["GET", "POST"])
def rate_movie():
    """
    Function handles the 'edit' button for each movie.
    """
    # Create new form.
    form = RateMovieForm()

    # Get the wanted movie to edit.
    movie_id = request.args.get('id')
    movie_to_update = db.session.query(Movies).get(movie_id)
    if movie_to_update is not None:  # If the movie was found.
        if form.validate_on_submit():  # Check if the form was sent successfully.
            # If so, try to edit the db to the new data.
            movie_to_update.rating = request.form['rating']
            movie_to_update.review = request.form['review']
            db.session.commit()
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


@app.route('/add', methods=['GET', 'POST'])
def add_movie():
    """
    Function finds movie list by movie title.
    :return: List of the movies, if found.
    """
    form = FindMovieForm()
    if form.validate_on_submit():
        movie_title = form.title.data  # Get the movies list that match the search.
        # Make an API call.
        response = requests.get(f"{MOVIE_DB_SEARCH_URL}", params={"api_key": TMDB_API_KEY, "query": movie_title})
        data = response.json()["results"]
        return render_template("select.html", movies=data)
    return render_template("add.html", form=form)


@app.route('/find')
def find_movie():
    """
    Function handles selection for particular movie in movies list.
    When the user clicks the desired movie, it will search the movie by ID
    and will add it to the DB with the title, img_url, year, description.
    :return: Redirect to homepage.
    """
    movie_api_id = request.args.get('id')
    if movie_api_id:  # Check if a movie id was entered.
        response = requests.get(f'https://api.themoviedb.org/3/movie/{movie_api_id}?api_key={TMDB_API_KEY}')
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


if __name__ == '__main__':
    app.run(debug=True)
