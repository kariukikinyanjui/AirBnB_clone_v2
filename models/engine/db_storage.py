#!/usr/bin/python3
"""This module defines the DBStorage class for the HBNB project."""
from os import getenv
from sqlalchemy import create_engine, MetaData
from sqlalchemy.orm import sessionmaker, scoped_session
from models.base_model import Base
from models.user import User
from models.state import State
from models.city import City
from models.amenity import Amenity
from models.place import Place
from models.review import Review


class DBStorage:
    """This class manages storage of the HBNB project in a MySQL database."""

    __engine = None
    __session = None

    def __init__(self):
        """Initialize the DBStorage instance."""
        user = getenv("HBNB_MYSQL_USER")
        passwd = getenv("HBNB_MYSQL_PWD")
        db = getenv("HBNB_MYSQL_DB")
        host = getenv("HBNB_MYSQL_HOST")
        env = getenv("HBNB_ENV")

        self.__engine = create_engine('mysql+mysqldb://{}:{}@{}/{}'.format(
            user, passwd, host, db),
            pool_pre_ping=True)

        if getenv('HBNB_ENV') == 'test':
            Base.metadata.drop_all(self.__engine)

    def all(self, cls=None):
        """Query all objects depending on the class name."""
        objects_dict = {}
        classes = [State, City, User, Place, Reveiw, Amenity]

        if cls is None:
            classes_to_query = classes
        else:
            classes_to_query = [cls]

        for class_ in classes_to_query:
            query_result = self.__session.query(class_).all()
            for obj in query_result:
                key = "{}.{}".format(obj.__class__.__name__, obj.id)
                objects_dict[key] = obj

            return objects_dict

    def new(self, obj):
        """Add the object to the current database session."""
        self.__session.add(obj)

    def save(self):
        """Commit all changes of the current database session."""
        self.__session.commit()

    def delete(self, obj=None):
        """Delete from the current database session."""
        if obj:
            self.__session.delete(obj)

    def reload(self):
        """Create all tables in the database and create the session."""
        Base.metadata.create_all(self.__engine)
        session_factory = sessionmaker(
                bind=self.__engine,
                expire_on_commit=False,
                )
        Session = scoped_session(session_factory)
        self.__session = Session()

    def close(self):
        """Call remove() on the private session attribute."""
        self.__session.close()
