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

def add_movie(title, genre_name):
    genre = session.query(Genre).filter_by(name=genre_name).first()
    if genre:
        new_movie = Movie(title=title, genre=genre)
        session.add(new_movie)
        session.commit()
    else:
        print(f"Genre '{genre_name}' not found. Please add the genre first.")


def borrow_movie(user_name, movie_title):
    user = session.query(User).filter_by(name=user_name).first()
    movie = session.query(Movie).filter_by(title=movie_title).first()
    if user and movie:
        user.borrowed_movies.append(movie)
        session.commit()
    else:
        print("User or movie not found. Please check the user and movie details.")


def delete_user(name):
    user = session.query(User).filter_by(name=name).first()
    if user:
        session.delete(user)
        session.commit()
        click.echo(f"User '{name}' deleted successfully.")
    else:
        click.echo(f"User '{name}' not found.")

def see_all_movies():
    movies = session.query(Movie).all()
    if movies:
        click.echo("\nAll Movies:")
        for movie in movies:
            click.echo(f"{movie.title} (Genre: {movie.genre.name})")
    else:
        click.echo("No movies in the database.")

