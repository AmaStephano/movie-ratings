"""Movie Ratings."""

from jinja2 import StrictUndefined

from flask import (Flask, jsonify,render_template, redirect, request, flash,
                   session)
from flask_debugtoolbar import DebugToolbarExtension

from model import User, Rating, Movie, connect_to_db, db


app = Flask(__name__)

# Required to use Flask sessions and the debug toolbar
app.secret_key = "ABC"

# Normally, if you use an undefined variable in Jinja2, it fails
# silently. This is horrible. Fix this so that, instead, it raises an
# error.
app.jinja_env.undefined = StrictUndefined


@app.route('/')
def index():
    """Homepage."""
    
    return render_template("homepage.html")

@app.route('/users')
def user_list():
    """Show list of users."""

    users = User.query.all()
    return render_template("user_list.html", users=users)

@app.route('/register', methods=["GET"])
def register_form():

    return render_template("/register_form.html")

@app.route('/register', methods=["POST"])
def register_process():

    email = request.form.get("email")
    password = request.form.get("password")
    age = request.form.get("age")
    zipcode = request.form.get("zipcode")

    check_user = User.query.filter(User.email == email).first()

    if check_user: 
        flash('This email already exists. Please log in.')
        return redirect("/login")
    else:
        new_user = User(email=email, password=password, age=age, zipcode=zipcode)
        db.session.add(new_user)
        db.session.commit()
        return redirect("/login")

@app.route('/login', methods=["GET"])
def login_form():

    return render_template("/login.html")


@app.route('/login', methods=["POST"])
def login_process():

    email = request.form.get("email")
    password = request.form.get("password")

    check_user = User.query.filter( (User.email == email) & (User.password == password) ).first()

    if check_user: 
        session['user_id'] = check_user.user_id
        flash("Logged in")
        user_page = "/users/" + str(session['user_id'])
        return redirect(user_page)
    else:
        flash("Incorrect email and/or password. Please try again.")
        return redirect("/login")

@app.route('/logout')
def log_out():

    session.pop('user_id', None)
    return render_template("/logout.html")

@app.route('/users/<user_id>')
def display_user_info(user_id):

    user_info = User.query.filter(User.user_id == user_id).first()
    rating_info = Rating.query.filter(Rating.user_id == user_id).all()

    return render_template("/user_details.html", user_info=user_info, rating_info=rating_info)

@app.route('/all_movies')
def display_all_movies():

    all_movies = Movie.query.order_by(Movie.title).all()

    return render_template("/all_movies.html", all_movies=all_movies)

@app.route('/all_movies/<unique_id>')
def display_user_info(unique_id):

    movie_info = Movie.query.filter_by(Movie.movie_id = unique_id).first()

    return render_template("/movie_details.html", movie_info=movie_info)


if __name__ == "__main__":
    # We have to set debug=True here, since it has to be True at the
    # point that we invoke the DebugToolbarExtension
    app.debug = True

    connect_to_db(app)

    # Use the DebugToolbar
    # DebugToolbarExtension(app)


    
    app.run()
