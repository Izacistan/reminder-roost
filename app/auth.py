from flask import Blueprint, render_template, request, flash, redirect, url_for
from . import db
from .models import User
from werkzeug.security import generate_password_hash, check_password_hash

auth = Blueprint('auth', __name__)


@auth.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        # Grab the provided data from the login form
        email = request.form.get('email')
        password = request.form.get('password')

        # Check if the provided email exists in the database
        user = User.query.filter_by(email=email).first()

        # If the user does exist, check that the provided password matches the hash in the database
        if user:
            if check_password_hash(user.password, password):
                flash("Logged in successfully!", category='success')
                return redirect(url_for('views.home'))
            else:
                flash("Incorrect password. Please try again", category='error')
        else:
            flash("No email found. Please try a different one.", category='error')



    return render_template("login.html")


@auth.route('/logout')
def logout():
    return "Logout page"


@auth.route('/sign-up', methods=['GET', 'POST'])
def sign_up():
    if request.method == 'POST':
        email = request.form.get('email')
        first_name = request.form.get('firstName')
        password_1 = request.form.get('password1')
        password_2 = request.form.get('password2')

        # Check if the provided email exists in the database
        user = User.query.filter_by(email=email).first()

        # If the provided email already exists, then we prevent a new account from being created. Else, validate the user input.
        if user:
            flash("This email is already being used.", category='error')
        elif len(email) < 4:
            flash('Email must be greater than 3 characters.', category='error')
        elif len(first_name) < 2:
            flash('First name must be greater than 1 character.', category='error')
        elif password_1 != password_2:
            flash('Passwords do not match.', category='error')
        elif len(password_1) < 7:
            flash('Password must be at least 7 characters', category='error')
        else:
            #Add user to the database (move to separate function)
            new_user = User(email=email, first_name=first_name, password=generate_password_hash(password_1, method='pbkdf2:sha256'))
            db.session.add(new_user)
            db.session.commit()
            flash(f"Account created for {first_name}!", category='success')

            # Redirect to URL for Home page
            return redirect(url_for('views.index'))

    return render_template("sign_up.html")
