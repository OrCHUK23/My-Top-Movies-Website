from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, FloatField
from wtforms.validators import DataRequired, NumberRange


class RateMovieForm(FlaskForm):
    rating = FloatField('Your Rating Out of 10:', validators=[DataRequired(), NumberRange(min=1, max=10,
                      message='Rating must be between 1 and 10.')], render_kw={"style": 'width: 10ch'})
    review = StringField('Your Review:', validators=[DataRequired()], render_kw={"style": 'width: 50ch'})
    submit = SubmitField('Done')


class FindMovieForm(FlaskForm):
    title = StringField('Movie Title', validators=[DataRequired()])
    submit = SubmitField('Add Movie')
