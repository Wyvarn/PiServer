import unittest
from datetime import datetime
from flask_login import current_user
from tests import BaseTestCase
from app.models import PiCloudUserAccount


class AuthTestCases(BaseTestCase):
    """
    Auth test cases
    """
    def test_login(self):
        """Test that the correct login data logs in the user"""
        with self.client:
            response = self.login()

            # check that there is a response
            self.assertTrue(response.status_code == 200)
            self.assertTrue(current_user.is_active)
            self.assertTrue(current_user.is_authenticated)

    def test_author_registration(self):
        """Test that a new user registration behaves as expected"""
        # todo: change redirects to True
        with self.client:
            self.client.post(
                'auth/register',
                data=dict(
                    email='picloudman@picloud.com',
                    password='password', confirm='password'
                ),
                follow_redirects=False
            )
            picloud_user = PiCloudUserAccount.query.filter_by(email='picloudman@picloud.com').first()
            self.assertTrue(picloud_user.id)
            self.assertTrue(picloud_user.email == 'picloucman@picloud.com')
            self.assertFalse(picloud_user.admin)

    # def test_get_author_by_id(self):
    #     """Ensure that the id is correct for the current logged in user"""
    #     with self.client:
    #         self.client.post("/login", data=dict(
    #             email='guydemaupassant@hadithi.com',
    #             password='password'
    #         ), follow_redirects=True)
    #         # self.assertTrue(current_user.id == 1)
    #         # self.assertFalse(current_user.id == 20)
    #
    # def test_registered_on_defaults_to_datetime(self):
    #     """Ensure that the registered_on date is a datetime object"""
    #     with self.client:
    #         self.client.post('/login', data=dict(
    #             email='guydemaupassant@hadithi.com',
    #             password='password'
    #         ), follow_redirects=True)
    #         author = AuthorAccount.query.filter_by(email='guydemaupassant@hadithi.com').first()
    #         self.assertIsInstance(author.registered_on, datetime)


if __name__ == '__main__':
    unittest.main()
