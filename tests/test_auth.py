import unittest
from datetime import datetime
from flask_login import current_user
from tests import BaseTestCase
from app.models import PiCloudUserAccount


class AuthTestCases(BaseTestCase):
    """
    Auth test cases
    """
    def test_picloud_login(self):
        """>>> Test that the correct login data logs in the user"""
        with self.client:
            response = self.login()

            # check that there is a response
            self.assertTrue(response.status_code == 200)
            self.assertTrue(current_user.is_active)
            self.assertTrue(current_user.is_authenticated)

    def test_picloud_registration(self):
        """>>> Test that a new user registration behaves as expected"""
        # todo: change redirects to True
        with self.client:
            self.client.post(
                'auth/register',
                data=dict(
                    email='picloudman@picloud.com',
                    password='picloudman', confirm='picloudman'
                ),
                follow_redirects=False
            )

            picloud_user_account = PiCloudUserAccount.query.filter_by(email='picloudman@picloud.com').first()
            self.assertTrue(picloud_user_account.get_id)
            self.assertTrue(picloud_user_account.email == 'picloudman@picloud.com')
            self.assertFalse(picloud_user_account.admin)

    def test_get_picloud_user_by_id(self):
        """>>> Ensure that the id is correct for the current logged in user"""
        with self.client:
            response = self.login()

            self.assertTrue(current_user.user_profile_id == 1)
            self.assertFalse(current_user.get_id == 20)

    # todo: implement this test
    # def test_validate_invalid_password(self):
    #     """>>> Test to ensure user can not log in with an invalid password"""
    #     with self.client:
    #         response = self.client.post("/login", data=dict(
    #             email='picloudman@picloud.com',
    #             password='picloudman'
    #         ), follow_redirects=True)
    #         # self.assertIn(b"Invalid email and/or password", response.data)

    def test_registered_on_defaults_to_datetime(self):
        """>>> Ensure that the registered_on date is a datetime object"""
        with self.client:
            self.client.post('auth/login', data=dict(
                email='picloudman@picloud.com',
                password='picloudman'
            ), follow_redirects=True)
            picloud_account = PiCloudUserAccount.query.filter_by(email='picloudman@picloud.com').first()
            self.assertIsInstance(picloud_account.registered_on, datetime)


if __name__ == '__main__':
    unittest.main()
