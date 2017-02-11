from sqlalchemy import Column, String, Integer, DateTime, func, ForeignKey, Boolean, event, DDL
from sqlalchemy.orm import relationship
from abc import ABCMeta, abstractmethod
import uuid
from sqlalchemy.ext.declarative import declared_attr
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin
from . import db, login_manager
from datetime import datetime


class Base(db.Model):
    """
    Base class for all the database tables, this class is used as a base for all the other classes
    Will contain abstract methods that will be common to all the other tables and databases
    Note that this implementation will be for basic tables such as UserAccount and UserProfile
    """
    __metaclass__ = ABCMeta
    __abstract__ = True

    id = Column(Integer, primary_key=True, autoincrement=True)
    date_created = Column(DateTime, default=func.current_timestamp())
    date_modified = Column(DateTime, default=func.current_timestamp(), onupdate=func.current_timestamp())

    @abstractmethod
    def __repr__(self):
        """
        Should return a human readable implementation of this object
        :return: Human readable representation of this object
        """
        pass


class PiCloudUserProfile(Base):
    """
    This will contain the user profile which is the actual user information
    such as name, email, accept terms of service, timezone, etc
    This will be the basic user profile
    :cvar __tablename__ the table name that will appear in the database
    :cvar first_name, the user's first name
    :cvar last_name, user's last name
    :cvar full_name, user's full name, which will be a combination of first and last names
    :cvar email, the user's email address
    :cvar accept_terms, whether the user has accepted the terms of service
    """
    __tablename__ = "user_profile"
    first_name = Column(String(255), nullable=False)
    last_name = Column(String(255), nullable=False)
    email = Column(String(500), nullable=False, unique=True)
    accept_terms = Column(Boolean, nullable=False, default=False)

    def __init__(self, first_name, last_name, email, accept_terms=False):
        """
        Return a new UserProfile object
        :param first_name: First name
        :param last_name: user's last name
        :param email: user's email
        """
        self.first_name = first_name
        self.last_name = last_name
        self.email = email
        self.accept_terms = accept_terms
        self.full_name = "{} {}".format(self.first_name, self.last_name)

    def __repr__(self):
        return "FullName: <FirstName: {}, LastName:{}>\n Email:{}\n".format(self.first_name,
                                                                            self.last_name, self.email)


class PiCloudUserAccount(db.Model, UserMixin):
    """
    User account table containing all sensitive account information, like passwords, username, etc
    :cvar uid, unique user id that will be auto-generated
    :cvar user_profile_id, the user account id that will be a foreign key and will be linked to
    UserProfile table
    :cvar username, the user's user name which will have a default value of email
    :cvar email, user email that will be linked to the UserProfile
    :cvar password_hash password that will be hashed and hidden
    :cvar admin, whether the user is an administrator in the system
    :cvar confirmed, whether this account has been confirmed
    :cvar confirmed_on, when this account was confirmed
    :cvar registered_on, when this account was first registered
    """
    __tablename__ = "user_account"
    uid = Column(String(250), default=str(uuid.uuid4()), nullable=False)
    user_profile_id = Column(Integer, ForeignKey(PiCloudUserProfile.id), primary_key=True,
                             autoincrement=True)
    username = Column(String(500), default=PiCloudUserProfile.email, nullable=True, unique=True)
    email = Column(String(500), default=PiCloudUserProfile.email, nullable=False, unique=True,
                   onupdate=PiCloudUserProfile.email)
    password_hash = Column(String(250), nullable=False)
    admin = Column(Boolean, nullable=True, default=False)
    registered_on = Column(DateTime, nullable=False)
    confirmed = Column(Boolean, nullable=False, default=False)
    confirmed_on = Column(DateTime, nullable=True)

    @property
    def registered(self):
        return self.registered_on

    @registered.setter
    def registered(self):
        """
        This sets the registered on attribute on the time that it is accessed using datetime.now()
        """
        self.registered_on = datetime.now()

    @property
    def password(self):
        """
        This is a property and should not be directly accessed, This is to protect the user password
        """
        raise AttributeError("password is not a readable attribute")

    @password.setter
    def password(self, password):
        """
        Sets the password for the user and generates a password hash
        :param password: user input password
        """
        self.password_hash = generate_password_hash(password)

    @password.getter
    def get_password(self):
        """
        Getter password attribute to fetch the password, This will return the hashed password however
        At no point will the real password be revealed
        """
        return self.password_hash

    def verify_password(self, password):
        """
        Verify a user's password to enable authentication into the system
        This will check the password hash against the input user password,
        :param password, the password to verify
        :return:
        """
        return check_password_hash(self.password_hash, password)

    def __repr__(self):
        """
        Return a formatted and human readable format
        :return: A human readable UserAccount object
        """
        return "ID <uid: {} User Profile Id: {}>\n Username: {}\n Email: {}\n Admin: {}\n Registered on:" \
               " {}\n Confirmed:< Is confirmed: {}, Date: {}>\n ".format(self.uid, self.user_profile_id,
                                                                         self.username, self.email,
                                                                         self.admin, self.registered_on,
                                                                         self.confirmed, self.confirmed_on)


@login_manager.user_loader
def load_user(user_id):
    """
    callback used to reload the user object from the user id stored in the session
    :param user_id: user id
    :return: User object stored in the session
    :rtype: PiCloudUserAccount
    """
    return PiCloudUserAccount.query.get(int(user_id))


# todo: add data metrics for checking who uploaded what when

class ExternalServiceAccount(db.Model):
    """
    The external service account is an abstract class that will contain information relating to
    external services such as Google Account, Facebook, Twitter, etc. This will be used to authenticate the
    user with such accounts and enable them to login with either of those accounts. Once the user is logged
    in then the relevant service account is updated and the UserAccount as well as UserProfiles will be
    updated as well
    """
    __metaclass__ = ABCMeta
    __abstract__ = True

    first_name = Column(String(250), nullable=False)
    last_name = Column(String(250), nullable=False)
    email = Column(String(500), nullable=False)

    def __init__(self, email, first_name, last_name):
        """
        Creates an ExternalServiceAccount object,
        :param email: The user email obtained from external auth account
        :param first_name: first name that will be returned from the authentication
        :param last_name: last name of the user
        """
        self.email = email
        self.first_name = first_name
        self.last_name = last_name

    @declared_attr
    def user_profile_id(self):
        """
        This is a declared attr, that will be used in all external accounts
        :return: UserAccount id that is a foreign and primary key
        """
        return Column(Integer, ForeignKey(PiCloudUserProfile.id), primary_key=True)


class FacebookAccount(ExternalServiceAccount):
    """
    Facebook account details for the author
    :cvar __tablename__: name of this table as represented in the database
    :cvar facebook_id: Facebook id received from
    """
    __tablename__ = "facebook_account"
    facebook_id = Column(String(100), nullable=True, unique=True)

    def __init__(self, facebook_id, email, first_name, last_name):
        super(FacebookAccount).__init__(email, first_name, last_name)
        self.facebook_id = facebook_id


class TwitterAccount(ExternalServiceAccount):
    """
    Twitter account table
    :cvar __tablename__: table name as rep in database
    :cvar twitter_id: The twitter id as set in Twitter, or as received from Twitter
    """
    __tablename__ = "twitter_account"
    twitter_id = Column(String(100), nullable=True, unique=True)

    def __init__(self, twitter_id, email, first_name, last_name):
        super(TwitterAccount).__init__(email, first_name, last_name)
        self.twitter_id = twitter_id


class GoogleAccount(ExternalServiceAccount):
    """
    Google Account table
    :cvar __tablename__: name of table in database
    :cvar google_id: Google id as received from Google on registration
    """
    __tablename__ = "google_account"
    google_id = Column(String(100), nullable=True, unique=True)

    def __init__(self, google_id, email, first_name, last_name):
        super(GoogleAccount).__init__(email, first_name, last_name)
        self.google_id = google_id


class AsyncOperationStatus(Base):
    """
    Dictionary table that stores 3 available statuses, pending, ok, error
    """
    __tablename__ = "async_operation_status"
    code = Column("code", String(20), nullable=True)

    def __repr__(self):
        return "Code: {}".format(self.code)


class AsyncOperation(Base):
    """

    """
    __tablename__ = "async_operation"
    async_operation_status_id = Column(Integer, ForeignKey(AsyncOperationStatus.id))
    user_profile_id = Column(Integer, ForeignKey(PiCloudUserProfile.id))

    status = relationship("AsyncOperationStatus", foreign_keys=async_operation_status_id)
    user_profile = relationship("PiCloudUserProfile", foreign_keys=user_profile_id)

    def __repr__(self):
        return "AsyncOpsId:{}, User Profile Id:{}, Status:{}, Profile:{}".format(
            self.async_operation_status_id, self.user_profile_id, self.status, self.user_profile)


event.listen(
    AsyncOperationStatus.__table__, "after_create",
    DDL(""" INSERT INTO async_operation_status (id,code) VALUES(1,'pending'),(2, 'ok'),(3, 'error'); """)
)
