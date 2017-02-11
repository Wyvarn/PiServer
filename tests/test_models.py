import unittest
from tests import BaseTestCase
from app.models import PiCloudUserAccount
from werkzeug.security import check_password_hash


class ModelTestCases(BaseTestCase):
    def test_check_password(self):
        """Ensure given password is correct after un-hashing"""
        picloud_user = PiCloudUserAccount.query.filter_by(email='picloudman@picloud.com').first()
        self.assertFalse(picloud_user.verify_password('admin'))
        self.assertFalse(picloud_user.verify_password('another_admin'))
        self.assertTrue(check_password_hash(picloud_user.get_password, "picloudman"))
        self.assertFalse(check_password_hash(picloud_user.get_password, "foobar"))

    # def test_validate_invalid_password(self):
    #     """Test to ensure user can not log in with an invalid password"""
    #     with self.client:
    #         response = self.client.post("/login", data=dict(
    #             email='picloudman@picloud.com',
    #             password='picloudman'
    #         ), follow_redirects=True)
    #         # self.assertIn(b"Invalid email and/or password", response.data)

    def test_password_verification(self):
        """_____Successfull password decryption should equal entered password"""
        picloud_user = PiCloudUserAccount(password='picloudman')
        self.assertTrue(picloud_user.verify_password('picloudman'))
        self.assertFalse(picloud_user.verify_password('dog'))

    def test_no_password_getter(self):
        """_____Checking password object of picloud_user after being set"""
        picloud_user = PiCloudUserAccount(password='picloudman')
        with self.assertRaises(AttributeError):
            picloud_user.password

    def test_password_setter(self):
        """_____Successful password property of picloud_user should not be none"""
        picloud_user = PiCloudUserAccount(password='picloudman')
        self.assertTrue(picloud_user.password_hash is not None)

    def test_password_salts_are_random(self):
        """_____Hashed passwords should not be the same"""
        picloud_user = PiCloudUserAccount(password='picloudman')
        user2 = PiCloudUserAccount(password='picloudman')
        self.assertTrue(picloud_user.password_hash != user2.password_hash)


if __name__ == "__main__":
    unittest.main()
