from sqlalchemy import Column, String, Integer, DateTime, func, ForeignKey, Boolean
from sqlalchemy.orm import relationship
from abc import ABCMeta, abstractmethod
import uuid
from sqlalchemy.ext.declarative import declared_attr
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

