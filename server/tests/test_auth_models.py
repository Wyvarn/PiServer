import unittest

from werkzeug.security import check_password_hash

from server.app import PiCloudUserAccount
from server.tests import BaseTestCase


class ModelTestCases(BaseTestCase):
    def test_check_password(self):
        """>>> Ensure given password is correct after un-hashing"""
        picloud_user = PiCloudUserAccount.query.filter_by(email='picloudman@picloud.com').first()
        self.assertFalse(picloud_user.verify_password('admin'))
        self.assertFalse(picloud_user.verify_password('another_admin'))
        self.assertTrue(check_password_hash(picloud_user.get_password, "picloudman"))
        self.assertFalse(check_password_hash(picloud_user.get_password, "foobar"))

    def test_password_verification(self):
        """>>> Successful password decryption should equal entered password"""
        picloud_user = PiCloudUserAccount(password='picloudman')
        self.assertTrue(picloud_user.verify_password('picloudman'))
        self.assertFalse(picloud_user.verify_password('dog'))

    def test_no_password_getter(self):
        """>>> Checking password object of picloud_user after being set"""
        picloud_user = PiCloudUserAccount(password='picloudman')
        with self.assertRaises(AttributeError):
            picloud_user.password

    def test_password_setter(self):
        """>>> Successful password property of picloud_user should not be none"""
        picloud_user = PiCloudUserAccount(password='picloudman')
        self.assertTrue(picloud_user.password_hash is not None)

    def test_password_salts_are_random(self):
        """>>> Hashed passwords should not be the same"""
        picloud_user = PiCloudUserAccount(password='picloudman')
        user2 = PiCloudUserAccount(password='picloudman')
        self.assertTrue(picloud_user.password_hash != user2.password_hash)

    def test_user_is_never_anonymous_(self):
        """>>> Tests that the user is never anonymous"""
        picloud_user = PiCloudUserAccount(password="picloudman")
        self.assertFalse(picloud_user.is_anonymous)


if __name__ == "__main__":
    unittest.main()
