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

class Movie(Base):
    __tablename__ = 'movies'
    id = Column(Integer, primary_key=True)
    title = Column(String)
    genre_id = Column(Integer, ForeignKey('genres.id'))
    genre = relationship('Genre', back_populates='movies')

class User(Base):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True)
    name = Column(String)
    borrowed_movies = relationship('Movie', secondary='borrowed_movies')

class BorrowedMovies(Base):
    __tablename__ = 'rented_movies'
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('users.id'))
    movie_id = Column(Integer, ForeignKey('movies.id'))

def create_database():
    Base.metadata.create_all(engine)


def search_movies(keyword):
    movies = session.query(Movie).filter(Movie.title.ilike(f'%{keyword}%')).all()
    return movies

def add_user(name):
    new_user = User(name=name)
    session.add(new_user)
    session.commit()


def add_genre(name):
    new_genre = Genre(name=name)
    session.add(new_genre)
    session.commit()