#!/usr/bin/python3
"""
defines a class FileStorage
"""
import json
from models.base_model import BaseModel
from models.user import User
from models.state import State
from models.city import City
from models.amenity import Amenity
from models.place import Place
from models.review import Review
from os import path


class FileStorage:
    """
    serializes instances to a JSON file
    and deserializes JSON file to instances
    Attr:
    __file_path - string - path to the JSON file
    __objects - dictionary - empty but will store all objects
    """
    __file_path = "file.json"
    __objects = {}
    class_dict = {"BaseModel": BaseModel, "User": User, "Place": Place,
                  "Amenity": Amenity, "City": City, "Review": Review,
                  "State": State}

    def all(self):
        """returns the dictionary __objects"""
        return self.__objects

    def new(self, obj):
        """sets in __objects the obj with key <obj class name>.id"""
        key = obj.__class__.__name__ + "." + obj.id
        self.__objects[key] = obj

    def save(self):
        """serializes __objects to the JSON file (path: __file_path)"""
        our_dict = {}
        for key, value in self.__objects.items():
            our_dict[key] = value.to_dict()
        with open(self.__file_path, mode="w", encoding="utf-8") as my_file:
            my_file.write(json.dumps(our_dict))

    def reload(self):
        """deserializes the JSON file to __objects"""
        try:
            with open(self.__file_path, mode="r", encoding="utf-8") as my_file:
                our_dict = json.load(my_file)
                for key, value in our_dict.items():
                    self.__objects[key] = self.class_dict[value["__class__"]](**value)
        except FileNotFoundError:
            pass
