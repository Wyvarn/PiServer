import unittest
from tests import BaseTestCase
from app.forms import LoginForm, RegisterForm, RecoverPasswordForm


class TestLoginForm(BaseTestCase):
    """
    Tests for login form
    """
    def test_correct_data_validates(self):
        """Test that the correct data is validated"""
        login_form = LoginForm(email="picloud_man@picloud.com", password="picloud_man")
        self.assertTrue(login_form.validate())

    def test_validate_invalid_email_format(self):
        """Test that invalid email format is not accepted by form"""
        login_form = LoginForm(email="picloud", password="picloud_mam")
        self.assertFalse(login_form.validate())

if __name__ == '__main__':
    unittest.main()
