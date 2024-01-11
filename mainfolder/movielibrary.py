from sqlalchemy import create_engine, Column, Integer, String, ForeignKey, Table
from sqlalchemy.orm import declarative_base, relationship, sessionmaker
import click
import os

Base = declarative_base()

engine = create_engine('sqlite:///movie_database.db', echo=False)
Session = sessionmaker(bind=engine)
session = Session()


class Genre(Base):
    __tablename__ = 'genres'
    id = Column(Integer, primary_key=True)
    name = Column(String)
    movies = relationship('Movie', back_populates='genre')
