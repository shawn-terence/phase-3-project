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
    rented_movies = relationship('Movie', secondary='rented_movies')

class BorrowedMovies(Base):
    __tablename__ = 'rented_movies'
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('users.id'))
    movie_id = Column(Integer, ForeignKey('movies.id'))

def create_database():
    from seed_data import add_seed_data
    Base.metadata.create_all(engine)
    add_seed_data(session)


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
        user.rented_movies.append(movie)
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

@click.command()
def main():
    create_database()

    while True:
        click.echo("\nMovie Database Management System")
        click.echo("1. Search Movies")
        click.echo("2. See All Movies")
        click.echo("3. Add User")
        click.echo("4. Add Genre")
        click.echo("5. Add Movie")
        click.echo("6. Rent a Movie")
        click.echo("7. Delete User")
        click.echo("8. Exit")
        choice = click.prompt("Enter your choice (1-8)", type=int)

        if choice == 1:
            keyword = click.prompt("Enter the keyword to search")
            movies = search_movies(keyword)
            if movies:
                click.echo("\nSearch Results:")
                for movie in movies:
                    click.echo(f"{movie.title} (Genre: {movie.genre.name})")
            else:
                click.echo("No movies found.")
        elif choice == 2:
            see_all_movies()
        elif choice == 3:
            name = click.prompt("Enter the user's name")
            add_user(name)
            click.echo(f"User '{name}' added successfully.")
        elif choice == 4:
            name = click.prompt("Enter the genre's name")
            add_genre(name)
            click.echo(f"Genre '{name}' added successfully.")
        elif choice == 5:
            title = click.prompt("Enter the movie's title")
            genre_name = click.prompt("Enter the genre's name")
            add_movie(title, genre_name)
            click.echo(f"Movie '{title}' added successfully.")
        elif choice == 6:
            user_name = click.prompt("Enter the user's name")
            movie_title = click.prompt("Enter the movie's title")
            borrow_movie(user_name, movie_title)
            click.echo(f"Movie '{movie_title}' rented by '{user_name}'.")
        elif choice == 7:
            name = click.prompt("Enter the user's name to delete")
            delete_user(name)
        elif choice == 8:
            save_data_to_files()
            click.echo("Data saved. Exiting Movie Database Management System. Goodbye!")
            break
        else:
            click.echo("Invalid choice. Please enter a number between 1 and 8.")
if __name__ == "__main__":
    main()
