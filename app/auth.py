from flask import Blueprint, render_template, request, flash, redirect, url_for
from . import db
from .models import User
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import login_user, login_required, logout_user, current_user #connected to user mix-in, in models.py

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

                # Log in the user
                login_user(user, remember=True)

                return redirect(url_for('views.index'))
            else:
                flash("Incorrect password. Please try again", category='error')
        else:
            flash("No email found. Please try a different one.", category='error')

    return render_template("login.html", user=current_user)


@auth.route('/logout')
@login_required
def logout():

    # Log out the current user
    logout_user()

    return redirect(url_for('auth.login'))


@auth.route('/sign-up', methods=['GET', 'POST'])
def sign_up():
    if request.method == 'POST':

        # These variables will be passed as arguments to future function, to be called here
        email = request.form.get('email')
        first_name = request.form.get('firstName')
        password_1 = request.form.get('password1')
        password_2 = request.form.get('password2')

        # Check if the provided email exists in the database
        user = User.query.filter_by(email=email).first()

        # Add this code to function later
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
            # Add user to the database (move to separate function)
            new_user = User(email=email, first_name=first_name,
                            password=generate_password_hash(password_1, method='pbkdf2:sha256'))

            # Add new user to the database
            db.session.add(new_user)
            db.session.commit()

            # Log in the user
            login_user(new_user, remember=True)

            flash(f"Account created for {first_name}!", category='success')

            # Redirect to URL for Home page
            return redirect(url_for('views.index'))

    return render_template("sign_up.html", user=current_user)
