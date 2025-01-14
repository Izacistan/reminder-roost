from flask import Blueprint, render_template, request, flash, redirect, url_for
from . import db
from .models import User
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import login_user, login_required, logout_user, current_user #connected to user mix-in, in models.py
from .utils.auth_func import validate_new_user_info

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

        # Validate the provided user information
        validation_result = validate_new_user_info(user, email, first_name, password_1, password_2)

        if validation_result:
            # Add user to the database (move to separate function)
            new_user = User(email=email, first_name=first_name, password=generate_password_hash(password_1, method='pbkdf2:sha256'))

            # Add new user to the database
            db.session.add(new_user)
            db.session.commit()

            # Log in the user
            login_user(new_user, remember=True)

            flash(f"Account created for {first_name}!", category='success')

            # Redirect to URL for Home page
            return redirect(url_for('views.index'))

    return render_template("sign_up.html", user=current_user)
