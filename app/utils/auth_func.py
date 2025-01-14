from flask import flash
import re


def validate_new_user_info(user, email, first_name, password_1, password_2):

    # Validate passwords and save in variable
    validate_pw_result = validate_new_password(password_1, password_2)

    if user:
        flash("This email is already being used.", category='error')
    elif len(email) < 4:
        flash('Email must be greater than 3 characters.', category='error')
    elif len(first_name) < 2:
        flash('First name must be greater than 1 character.', category='error')
    elif not validate_pw_result:
        return False
    else:
        # All criteria are met, return `True` to add new user
        return True


def validate_new_password(password_1, password_2):
    """
    Validate that two provided passwords meet security criteria.

    Args:
        password_1 (str): The first password input.
        password_2 (str): The second password input to confirm they match.

    Returns:
        bool: True if the passwords meet all criteria, otherwise False.

    Security Criteria:
        - Passwords must match.
        - Must be at least 8 characters long.
        - Must contain at least one uppercase letter.
        - Must contain at least one lowercase letter.
        - Must contain at least one digit.
        - Must contain at least one special character from the set: "!@#$%^&*(),.?\":{}|<>".

    @todo Instead o flashing a message here, create a an error message variable with corresponding error message, which will be flashed outside of the function, if needed.

    Flash Messages:
        - Displays success or specific error messages to the user based on the validation outcome.
    """
    if password_1 != password_2:
        # flash('Passwords do not match.', category='error')
        return False
    elif len(password_1) < 8:
        # flash('Password must be at least 8 characters', category='error')
        return False
    elif not re.search(r'[A-Z]', password_1):  # Uppercase letter
        # flash('Password must contain at least one uppercase character.', category='error')
        return False
    elif not re.search(r'[a-z]', password_1):  # Lowercase letter
        # flash('Password must contain at least one lowercase character.', category='error')
        return False
    elif not re.search(r'[0-9]', password_1):  # Digit
        # flash('Password must contain at least one number.', category='error')
        return False
    elif not re.search(r'[!@#$%^&*(),.?":{}|<>]', password_1):  # Special character
        # flash('Password must at least one special character: "!@#$%^&*(),.?":{}|<>".', category='error')
        return False
    else:
        # flash('Passwords validated. Success!', category='success')
        return True
