from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from movielibrary import Base, Genre, Movie, User, BorrowedMovies

def add_seed_data(session):
    if session.query(Genre).count() > 0:
        print("Seed data already exists. Skipping.")
        return
    
    # Genres
    action_genre = Genre(name="Action")
    drama_genre = Genre(name="Drama")
    comedy_genre = Genre(name="Comedy")
    adventure_genre = Genre(name="Adventure")
    fantasy_genre = Genre(name="Fantasy")

    # Movies
    movie1 = Movie(title="Inception", genre=action_genre)
    movie2 = Movie(title="The Dark Knight", genre=action_genre)
    movie3 = Movie(title="The Shawshank Redemption", genre=drama_genre)
    movie4 = Movie(title="Forrest Gump", genre=drama_genre)
    movie5 = Movie(title="Monty Python and the Holy Grail", genre=comedy_genre)
    movie6 = Movie(title="Anchorman: The Legend of Ron Burgundy", genre=comedy_genre)
    movie7 = Movie(title="Indiana Jones: Raiders of the Lost Ark", genre=adventure_genre)
    movie8 = Movie(title="Jurassic Park", genre=adventure_genre)
    movie9 = Movie(title="The Lord of the Rings: The Fellowship of the Ring", genre=fantasy_genre)
    movie10 = Movie(title="Harry Potter and the Sorcerer's Stone", genre=fantasy_genre)

    # Users
    user1 = User(name="Alice")
    user2 = User(name="Bob")
    user3 = User(name="Pete")

    session.add_all([
        action_genre, drama_genre, comedy_genre, adventure_genre, fantasy_genre,
        movie1, movie2, movie3, movie4, movie5, movie6, movie7, movie8, movie9, movie10,
        user1, user2
    ])
    session.commit()

if __name__ == "__main__":
    engine = create_engine('sqlite:///movie_database.db', echo=False)
    Base.metadata.create_all(engine)
    
    Session = sessionmaker(bind=engine)
    session = Session()

    add_seed_data(session)

    print("Seed data added successfully.")
