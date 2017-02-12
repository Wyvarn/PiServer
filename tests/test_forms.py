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


class TestRegisterForm(BaseTestCase):
    """
    Tests for RegisterForm

    """

    def test_validate_successful_register(self):
        """Test the correct data is validated"""
        form = RegisterForm(
            first_name="picloud",
            last_name="man",
            email="picloud_man@picloud.com",
            password="picloudman",
            verify_password="picloudman"
        )
        self.assertTrue(form.validate())

    def test_checks_for_invalid_password_lengths(self):
        """Checks that invalid password lengths are not allowed"""
        form = RegisterForm(
            first_name="picloud",
            last_name="man",
            email="picloud_man@picloud.com",
            password="picl",
            verify_password="picl"
        )
        self.assertFalse(form.validate())

    def test_validate_email_already_registerd(self):
        """Test that register form does not validate an already registerd email address"""
        form = RegisterForm(
            first_name="picloud",
            last_name="man",
            email="picloud_man@picloud.com",
            password="picloud",
            verify_password="picloud"
        )
        self.assertFalse(form.validate_form())

    def test_validate_both_passwords_match(self):
        """Tests that both passwords should match"""
        form = RegisterForm(
            first_name="picloud",
            last_name="man",
            email="picloud_man@picloud.com",
            password="piclould",
            verify_password="picl"
        )
        self.assertFalse(form.validate())

if __name__ == '__main__':
    unittest.main()
