from sqlalchemy import Column, Integer, String, Float
from sqlalchemy_utils import URLType
from config import db


class Movies(db.Model):
    """
    This class is for the Movies sheet.
    """
    id = Column(Integer, primary_key=True)
    title = Column(String, unique=True, nullable=False)
    year = Column(Integer, nullable=False)
    description = Column(String, unique=True, nullable=False)
    rating = Column(Float, nullable=False)
    ranking = Column(Integer, nullable=False)
    review = Column(String, nullable=False)
    img_url = Column(URLType, nullable=False)