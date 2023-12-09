"""Server for movie ratings app."""

from flask import (Flask, render_template, request, flash, session,
                   redirect)
from model import connect_to_db, db
import crud
from jinja2 import StrictUndefined

app = Flask(__name__)
app.secret_key = "dev"
app.jinja_env.undefined = StrictUndefined


@app.route('/')
def homepage():
    """View homepage."""

    return render_template('homepage.html')


@app.route('/movies')
def show_all_movies():
    """View all movies."""

    movies = crud.get_movies()

    return render_template('all_movies.html', movies=movies)


@app.route("/movie/<movie_id>")
def show_movie(movie_id):
    """Show details on a particular movie."""

    print("**********************************")
    print(f'movie_id = {movie_id}')
    print("*********************************")
    movie = crud.get_movie_by_id(movie_id)


    return render_template("movie_details.html", movie=movie)

#@app.route("/movie/<movie_id>/add_rating", #method=['POST']#)
@app.route("/add_rating/<movie_id>")
def rate_movie(movie_id):
    """Add a movie rating."""

    print()
    print()
    print("**********************************")
    print(f'movie_id = {movie_id}')
    print("*********************************")
    print()
    print()

    score = request.form.get('#rating-select')
    print()
    print()
    print("**********************************")
    print(f'score = {score}')
    print("*********************************")
    print()
    print()

    rating = crud.get_rating_by_user(session['user'], movie_id)

    # #if the user is logged in and they have not rated this movie yet
    # if session['user']:
    #     pass
    # #if the user is logged in but already left a rating

    # #if there is not a user logged in
    #if user not in session:
     #   flash("You must be logged in to rate a movie.")
      #  return redirect("/login_users")
        

    return redirect("/movies")


@app.route('/users')
def show_all_users():
    """View all users."""

    users = crud.get_users()

    return render_template('all_users.html', users=users)


@app.route('/users', methods=["POST"])
def create_users():
    """Create users."""

    email = request.form.get('email')
    password = request.form.get('password')

    if crud.get_user_by_email(email):
        flash("This email is already attached to an account.")
    else:
        new_user = crud.create_user(email=email, password=password)
        db.session.add(new_user)
        db.session.commit()
        flash("Your account was successfully made. You can now log in.")

    return redirect("/")


@app.route('/login', methods=["POST"])
def login_users():
    """Login users."""

    email = request.form.get('email')
    password = request.form.get('password')

    user = crud.get_user_by_email(email)

    if user and user.password == password:
        session['user'] = user.user_id
        flash("You were successfully logged in.")
    elif user and user.password != password:
        flash("Your email and password do not match")
    else:
        flash("This user does not exist.")

    return redirect("/")


@app.route("/user/<user_id>")
def show_user(user_id):
    """Show details on a particular user."""

    user = crud.get_user_by_id(user_id)

    return render_template("user_details.html", user=user)


if __name__ == "__main__":
    connect_to_db(app)
    app.run(host="0.0.0.0", debug=True)
