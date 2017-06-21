import unittest
from app import create_app, db
from app.models import PiCloudUserAccount, PiCloudUserProfile
from flask_testing import TestCase
from sqlalchemy.exc import IntegrityError
from datetime import datetime
from flask import url_for


class ContextTestCase(TestCase):
    """
    Handles context test cases for the application
    """
    render_templates = True

    def create_app(self):
        app = create_app("testing")
        app.config['PRESERVE_CONTEXT_ON_EXCEPTION'] = False
        return app

    def _pre_setup(self):
        self.app = create_app('testing')
        self.client = self.app.test_client()

    def __call__(self, result=None):
        try:
            self._pre_setup()
            super(ContextTestCase, self).__call__(result)
        finally:
            self._post_teardown()

    def _post_teardown(self):
        if getattr(self, '_ctx', None) and self._ctx is not None:
            self._ctx.pop()
            del self._ctx


class BaseTestCase(ContextTestCase):
    """
    Base test case for application
    This base test case will setup the datbase, enable login and configure adding files accessing them
    of course all this will be dummy
    """

    def setUp(self):
        self.app_context = self.app.app_context()
        self.app_context.push()
        self.db = db

        db.create_all()

        self.create_user_account()
        # self.add_file()

        db.session.commit()

    def tearDown(self):
        db.session.remove()
        db.drop_all()
        self.app_context.pop()

    @staticmethod
    def create_user_account():
        """
        Creates a dummy account to use for tests
        :return: a new UserProfile Account
        :rtype: PiCloudUserProfile
        """
        # get a user object
        user_profile = PiCloudUserProfile.query.filter_by(email="picloudman@picloud.com").first()

        # if the user is none, create one, this most likely means that the user account is none as well
        if user_profile is None:
            try:
                user_profile = PiCloudUserProfile(first_name="picloud", last_name="man",
                                                  email="picloudman@picloud.com")
                user_account = PiCloudUserAccount(username="picloud", email=user_profile.email,
                                                  password="picloudman", registered_on=datetime.now())
                db.session.add(user_account)
                db.session.add(user_profile)
            except IntegrityError as ie:
                print(ie)
                db.session.rollback()

        return user_profile

    def login(self):
        """
        Login in the user to the testing app
        :return: The authenticated user for the test app
        """
        # todo, change follow_redirects to TRUE
        return self.client.post(
            "auth/login",
            data=dict(
                email='picloudman@picloud.com',
                password='picloudman',
            ),
            follow_redirects=False
        )

    # todo: add dummy adding file and dummy downloading file

if __name__ == "__main__":
    unittest.main()
