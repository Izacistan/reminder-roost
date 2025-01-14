import unittest
from reminder_roost.app.utils.auth_func import validate_new_password


class TestValidateNewPassword(unittest.TestCase):
    def test_passwords_do_not_match(self):
        # Passwords are not the same
        self.assertFalse(validate_new_password("Password123!", "Password321!"))

    def test_password_too_short(self):
        # Password is less than 8 characters
        self.assertFalse(validate_new_password("Short1!", "Short1!"))

    def test_missing_uppercase(self):
        # Password lacks an uppercase letter
        self.assertFalse(validate_new_password("password123!", "password123!"))

    def test_missing_lowercase(self):
        # Password lacks a lowercase letter
        self.assertFalse(validate_new_password("PASSWORD123!", "PASSWORD123!"))

    def test_missing_digit(self):
        # Password lacks a digit
        self.assertFalse(validate_new_password("Password!", "Password!"))

    def test_missing_special_character(self):
        # Password lacks a special character
        self.assertFalse(validate_new_password("Password123", "Password123"))

    def test_valid_password(self):
        # Password meets all criteria
        self.assertTrue(validate_new_password("Password123!", "Password123!"))

    def test_invalid_special_character(self):
        # Special character check for validity beyond listed set (if applicable)
        self.assertFalse(validate_new_password("Password123~", "Password123~"))

    def test_password_with_spaces(self):
        # Check spaces are allowed as part of the password
        self.assertTrue(validate_new_password("Password 123!", "Password 123!"))


if __name__ == "__main__":
    unittest.main()
