#!/usr/bin/python3
"""
Contains the class DBStorage
"""

import models
from models.amenity import Amenity
from models.base_model import BaseModel, Base
from models.city import City
from models.place import Place
from models.review import Review
from models.state import State
from models.user import User
from os import getenv
import sqlalchemy
from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker

classes = {"Amenity": Amenity, "City": City,
           "Place": place.Place, "Review": review.Review, "State": state.State, "User": user.User}


class DBStorage:
    classes = {"Amenity": Amenity, "City": City, base_model.BaseModel
           "Place": Place, "Review": Review, "State": State, "User": User}

    """interaacts with the MySQL database"""
    __engine = None
    __session = None

    def __init__(self):
        """Instantiate a DBStorage object"""
        HBNB_MYSQL_USER = getenv('HBNB_MYSQL_USER')
        HBNB_MYSQL_PWD = getenv('HBNB_MYSQL_PWD')
        HBNB_MYSQL_HOST = getenv('HBNB_MYSQL_HOST')
        HBNB_MYSQL_DB = getenv('HBNB_MYSQL_DB')
        HBNB_ENV = getenv('HBNB_ENV')
        self.__engine = create_engine('mysql+mysqldb://{}:{}@{}/{}'.
                                      format(HBNB_MYSQL_USER,
                                             HBNB_MYSQL_PWD,
                                             HBNB_MYSQL_HOST,
                                             HBNB_MYSQL_DB))
        if HBNB_ENV == "test":
            Base.metadata.drop_all(self.__engine)

    def all(self, cls=None):
        """ returns a dictionary of all objects """
        cls_dict = {}
        if cls:
            obj_class = self.__session.query(self.classes.get(cls)).all()
            for item in obj_class:
                key = str(item.__class__.__name__) + "." + str(item.id)
                cls_dict[key] = item
            return cls_dict
        for class_name in self.classes:
            if class_name == 'BaseModel':
                continue
            obj_class = self.__session.query(
                self.classes.get(class_name)).all()
            for item in obj_class:
                key = str(item.__class__.__name__) + "." + str(item.id)
                cls_dict[key] = item
        return cls_dict

    def get(self, cls, id):
        """
        obtains a spercific object using ID
        """
        all_cls = self.all(cls)

        for obj in all_cls.values():
            if id == str(obj.id):
                return obj

        return None

    def count(self, cls=None):
        """
        counts the number of instance of a class
        """
        return len(self.all(cls))



    def new(self, obj):
        """add the object to the current database session"""
        self.__session.add(obj)

    def save(self):
        """commit all changes of the current database session"""
        self.__session.commit()

    def delete(self, obj=None):
        """delete from the current database session obj if not None"""
        if obj is not None:
            self.__session.delete(obj)

    def reload(self):
        """reloads data from the database"""
        Base.metadata.create_all(self.__engine)
        sess_factory = sessionmaker(bind=self.__engine, expire_on_commit=False)
        Session = scoped_session(sess_factory)
        self.__session = Session

    def close(self):
        """call remove() method on the private session attribute"""
        self.__session.remove()
