"""Script to seed database."""

import os
import json
from random import choice, randint
from datetime import datetime

import crud
import model
import server

# More code will go here

#The first thing you do when re-creating a database is run dropdb and createdb. 
#You can get Python to run those commands for you using os.system. Add the following lines of code to seed_database.py.
os.system('dropdb ratings')
os.system('createdb ratings')

#connect to the database and call db.create_all
model.connect_to_db(server.app)
model.db.create_all()

#load data from data/movies.json and save it to a variable

with open('data/movies.json') as f:
    movie_data = json.loads(f.read())

# Create movies, store them in list so we can use them
# to create fake ratings later
movies_in_db = []
for movie in movie_data:
    # TODO: get the title, overview, and poster_path from the movie
    # dictionary. Then, get the release_date and convert it to a
    # datetime object with datetime.strptime
    title = movie['title']
    overview = movie['overview']
    poster_path = movie['poster_path']
    date = movie['release_date']
    #YYYY-MM-DD
    format = '%Y-%m-%d'

    #convert date here
    date = datetime.strptime(date, format)

    # TODO: create a movie here and append it to movies_in_db
    movie = crud.create_movie(title=title, 
                  overview=overview, 
                  poster_path=poster_path, 
                  release_date = date)

    movies_in_db.append(movie)

model.db.session.add_all(movies_in_db)
model.db.session.commit()


ratings_in_db = []

for n in range(10):
    email = f'user{n}@test.com'  # Voila! A unique email!
    password = 'test'

    user = crud.create_user(email,password)
    model.db.session.add(user)

    # TODO: create 10 ratings for the user

    for r in range(10):
        random_movie = choice(movies_in_db)
        score = randint(1,5)

        rating = crud.create_rating(score, random_movie.movie_id, user.user_id)
        ratings_in_db.append(rating)

model.db.session.add_all(ratings_in_db) 

model.db.session.commit()



  
