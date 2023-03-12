#!/usr/bin/python3
"""
defines BaseModel class
"""
import uuid
from datetime import datetime
import models


class BaseModel:
    """
    defines all common attributes/methods for other classes
    Attr:
    id - assigns unique id
    created_at - assign with the current datetime when an instance is created
    updated_at - datetime - assign with the current datetime when an instance
    is created and it will be updated every time you change your object
    """
    def __init__(self, *args, **kwargs):
        """ instantiation"""
        if kwargs:
            for key, value in kwargs.items():
                if key in ("created_at", "updated_at"):
                    value = datetime.strptime(value, "%Y-%m-%dT%H:%M:%S.%f")

                if key != "__class__":
                    setattr(self, key, value)

        else:
            self.id = str(uuid.uuid4())
            self.created_at = datetime.now()
            self.updated_at = self.created_at
            models.storage.new(self)

    def __str__(self):
        """
        representation of a class string
        """
        return "[{0}] ({1}) {2}".format(self.__class__.__name__, self.id, self.__dict__)

    def save(self):
        """
        updates the public instance attr updated_at with the current datetime
        """
        self.updated_at = datetime.now()
        models.storage.save()

    def to_dict(self):
        """
        returns a dictionary containing all keys/values
        of __dict__ of the instance
        """
        class_info = self.__dict__.copy()
        class_info['__class__'] = self.__class__.__name__
        class_info['created_at'] = self.created_at.isoformat()
        class_info['updated_at'] = self.updated_at.isoformat()

        return class_info
