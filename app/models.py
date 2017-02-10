from sqlalchemy import Column, String, Integer, DateTime, func, ForeignKey, Boolean
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
        :return: Human readable representaion of this object
        """
        pass


class UserProfile(Base):
    """
    This will contain the user profile which is the actual user information
    such as name, email, accept terms of service, timezone, etc
    This will be the basic user profile
    :cvar __tablename__ the table name that will appear in the database
    :cvar first_name, the user's first name
    :cvar last_name, user's last name
    :cvar full_name, user's full name, which will be a combination of first and last names
    :cvar email, the user's email address
    :cvar whether the user has accepted the terms of service
    """
    __tablename__ = "user_profile"
    first_name = Column(String(255), nullable=False)
    last_name = Column(String(255), nullable=False)
    full_name = "{} {}".format(first_name, last_name)
    email = Column(String(500), nullable=False, unique=True)
    accept_terms = Column(Boolean, nullable=False, default=False)

    def __repr__(self):
        return "FullName: <FirstName: {}, LastName:{}>\n Email:{}\n".format(self.first_name,
                                                                            self.last_name, self.email)


class UserAccount(db.Model):
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
    user_profile_id = Column(Integer, ForeignKey(UserProfile.id), primary_key=True)
    username = Column(String(500), default=UserProfile.email, nullable=True, unique=True)
    email = Column(String(500), default=UserProfile.email, nullable=False, unique=True, onupdate=UserProfile.email)
    password_hash = Column(String(250), nullable=False)
    admin = Column(Boolean, nullable=True, default=False)
    registered_on = Column(DateTime, nullable=False)
    confirmed = Column(Boolean, nullable=False, default=False)
    confirmed_on = Column(DateTime, nullable=True)

    @property
    def password(self):
        raise AttributeError("password is not a readable attribute")

    @password.setter
    def password(self, password):
        """
        Sets the password for the user and generates a password hash
        :param password: user input password
        """
        self.password_hash = generate_password_hash(password)

    @password.getter
    def password(self):
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
    :rtype: UserAccount
    """
    return UserAccount.query.get(int(user_id))


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
        return Column(Integer, ForeignKey(UserProfile.id), primary_key=True)


    