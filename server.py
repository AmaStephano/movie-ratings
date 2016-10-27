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

    check_user = User.query.filter(User.email == email).first()

    if check_user: 
        flash('Please try a different email. This email is already registered.')
        return redirect("/register")
    else:
        new_user = User(email=email, password=password)
        db.session.add(new_user)
        db.session.commit()
        return redirect("/")

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
        return redirect("/")
    else:
        flash("Incorrect email and/or password. Please try again.")
        return redirect("/login")

@app.route('/logout')
def log_out():

    session.pop('user_id', None)
    return render_template("/logout.html")


if __name__ == "__main__":
    # We have to set debug=True here, since it has to be True at the
    # point that we invoke the DebugToolbarExtension
    app.debug = True

    connect_to_db(app)

    # Use the DebugToolbar
    # DebugToolbarExtension(app)


    
    app.run()
