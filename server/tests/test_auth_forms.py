import unittest

from server.app import LoginForm, RegisterForm, RecoverPasswordForm, ChangePasswordForm
from server.tests import BaseTestCase


class TestLoginForm(BaseTestCase):
    """
    Tests for login form
    """

    def test_correct_data_validates(self):
        """>>> Test that the correct data is validated"""
        login_form = LoginForm(email="picloud_man@picloud.com", password="picloud_man")
        self.assertTrue(login_form.validate())

    def test_validate_invalid_email_format(self):
        """>>> Test that invalid email format is not accepted by form"""
        login_form = LoginForm(email="picloud", password="picloud_mam")
        self.assertFalse(login_form.validate())

    def test_validate_invalid_password_input(self):
        """>>> Test that form does not validate empty password field"""
        login_form = LoginForm(email="picloud@picloud.com", password="")
        self.assertFalse(login_form.validate())

    def test_validate_empty_password_input(self):
        """>>> Tests that the form does not validate empty email input"""
        login_form = LoginForm(email="", password="picloud_man")
        self.assertFalse(login_form.validate())


class TestRegisterForm(BaseTestCase):
    """
    Tests for RegisterForm

    """

    def test_validate_successful_register(self):
        """>>> Test the correct data is validated"""
        form = RegisterForm(
            first_name="picloud",
            last_name="man",
            email="picloud_man@picloud.com",
            password="picloudman",
            verify_password="picloudman"
        )
        self.assertTrue(form.validate())

    def test_checks_for_invalid_password_lengths(self):
        """>>> Checks that invalid password lengths are not allowed"""
        form = RegisterForm(
            first_name="picloud",
            last_name="man",
            email="picloud_man@picloud.com",
            password="picl",
            verify_password="picl"
        )
        self.assertFalse(form.validate())

    def test_validate_email_already_registered(self):
        """>>> Test that register form does not validate an already registerd email address"""
        form = RegisterForm(
            first_name="picloud",
            last_name="man",
            email="picloud_man@picloud.com",
            password="picloud",
            verify_password="picloud"
        )
        self.assertFalse(form.validate_form())

    def test_validate_both_passwords_match(self):
        """>>> Tests that both passwords should match"""
        form = RegisterForm(
            first_name="picloud",
            last_name="man",
            email="picloud_man@picloud.com",
            password="piclould",
            verify_password="picl"
        )
        self.assertFalse(form.validate())


class TestRecoverPassword(BaseTestCase):
    """
    Tests for recover password form
    """

    def test_validates_email(self):
        """>>> Test that the form validates the email input"""
        form = RecoverPasswordForm(
            email="picloud_man@picloud.com"
        )
        self.assertTrue(form.validate())

    def test_validate_invalid_email(self):
        """>>> Test that the form does not submit if the email is not valid"""
        form = RecoverPasswordForm(
            email="picloud"
        )
        self.assertFalse(form.validate())

    def test_validate_empty_email_input(self):
        """>>> Tests that the form does not validate and empty email field"""
        form = RecoverPasswordForm(
            email=""
        )
        self.assertFalse(form.validate())

    def test_validate_email_non_existent(self):
        """>>> Test that recover password form does not validate a non existent email address"""
        form = RecoverPasswordForm(email="picloud_man@picloud.com")
        self.assertFalse(form.validate_form())

    def test_validate_email_exists(self):
        """>>> Test that recover password form validates an existent email address"""
        form = RecoverPasswordForm(email="picloudman@picloud.com")
        self.assertTrue(form.validate_form())


class TestChangePasswordForm(BaseTestCase):
    """
    Tests for changing password form
    """

    def test_validates_email(self):
        """>>> Tests that the form validates email input"""
        form = ChangePasswordForm(email="picloudman@picloud.com",
                                  password_field_1="picloudawesome", password_field_2="picloudawesome")
        self.assertTrue(form.validate())

    def test_validates_empty_email_input(self):
        """>>> Tests that empty email input is not validated"""
        form = ChangePasswordForm(email="",
                                  password_field_1="picloudawesome", password_field_2="picloudawesome")
        self.assertFalse(form.validate())

    def test_validates_invalid_email_input(self):
        """>>> test that invalid email inputs are not validated"""
        form = ChangePasswordForm(email="picloudman",
                                  password_field_1="picloudawesome", password_field_2="picloudawesome")
        self.assertFalse(form.validate())

    def test_validates_password_fields_match(self):
        """>>> test that the password fields match"""
        form = ChangePasswordForm(email="picloudman@picloud.com",
                                  password_field_1="picloudawesome", password_field_2="picloudawesome")
        self.assertEqual(form.password_field_1.data, form.password_field_2.data)
        self.assertTrue(form.validate())

    def test_validates_password_fields_dont_match(self):
        """>>> Test that the password fields do not match"""
        form = ChangePasswordForm(email="picloudman@picloud.com",
                                  password_field_1="picloudawesome", password_field_2="picloudawesome2")
        self.assertFalse(form.validate())


if __name__ == '__main__':
    unittest.main()
