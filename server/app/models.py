"""
Base models for application. Will be used to provide a single source of truth for the
models in the application
"""
from sqlalchemy import Column, Integer, DateTime, func
from abc import ABCMeta, abstractmethod
from . import db


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