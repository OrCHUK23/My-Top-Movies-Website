## Flask Movie Collection App

This is a Flask web application for managing and rating movies. Users can add movies to their collection, rate them, and write reviews. The application utilizes SQLAlchemy for database management and Flask-WTF for form handling.

### Project Structure

The project directory structure is as follows:

- `app.py`: The main Flask application file.
- `forms.py`: Contains the Flask-WTF form definitions.
- `models.py`: Defines the SQLAlchemy models for the movies.
- `config.py`: Configures the SQLite database and initializes SQLAlchemy.
- `templates/`: Directory containing the HTML templates for the web pages.
  - `index.html`: Displays the user's top-rated movies.
  - `add.html`: Allows users to add a new movie to their collection.
  - `select.html`: Displays a list of movies to select from.
  - `rate_movie.html`: Enables users to rate and review a movie.
  - `movie_details.html`: Shows detailed information about a movie.
- `static/`: Directory containing static files such as CSS stylesheets and images.
  - `css/styles.css`: CSS styles for the application.
  
### Installation

To run the application, follow these steps:

1. Clone the repository: `git clone https://github.com/OrCHUK23/My-Top-Movies-Website.git`
2. Install the required packages: `pip install -r requirements.txt`
3. Run the Flask development server: `flask run`

Make sure to update the `DATABASE_URI` in `config.py` to match your desired database location.

### Dependencies

The following dependencies are listed in the `requirements.txt` file:

async-generator==1.10
attrs==22.2.0
blinker==1.6.2
certifi==2023.5.7
cffi==1.15.1
charset-normalizer==3.1.0
click==8.1.3
colorama==0.4.6
dominate==2.7.0
exceptiongroup==1.1.1
Flask==2.3.2
Flask-Bootstrap==3.3.7.1
Flask-SQLAlchemy==3.0.3
Flask-WTF==1.1.1
greenlet==2.0.2
h11==0.14.0
idna==3.4
itsdangerous==2.1.2
Jinja2==3.1.2
MarkupSafe==2.1.2
outcome==1.2.0
pycparser==2.21
PySocks==1.7.1
python-dotenv==1.0.0
requests==2.30.0
selenium==4.8.3
selenium-stealth==1.0.6
sniffio==1.3.0
sortedcontainers==2.4.0
SQLAlchemy==2.0.13
SQLAlchemy-Utils==0.41.1
trio==0.22.0
trio-websocket==0.10.2
typing_extensions==4.5.0
undetected-chromedriver==3.4.6
urllib3==2.0.2
visitor==0.1.3
websockets==11.0.1
Werkzeug==2.3.4
wsproto==1.2.0
WTForms==3.0.1

### HTML Templates

Here are the HTML templates used in the application:

- `index.html`: Displays the user's top-rated movies.
- `add.html`: Allows users to add a new movie to their collection.
- `select.html`: Displays a list of movies to select from.
- `rate_movie.html`: Enables users to rate and review a movie.
- `movie_details.html`: Shows detailed information about a movie.

### CSS Styles
The CSS styles for the application can be found in the `styles.css` file located in the `static/css/` directory.

### Usage
1. Access the application by visiting `http://localhost:5000` in your web browser.
2. Navigate to the different pages using the provided links and buttons.
3. Add new movies, rate them, and write reviews.
4. Enjoy managing your movie collection!
