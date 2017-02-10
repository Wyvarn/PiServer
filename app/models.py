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
    email = Column(String(500), nullable=False)
    accept_terms = Column(Boolean, nullable=False, default=False)

    def __repr__(self):
        return "FullName: <FirstName: {}, LastName:{}>\n Email:{}\n".format(self.first_name,
                                                                            self.last_name, self.email)

