#!/usr/bin/python3
"""
defines a class User that inherits from BaseModel class
"""
from models.base_model import BaseModel


class User(BaseModel):
    """
    Attr:
    email: string - empty string
    password: string - empty string
    first_name: string - empty string
    last_name: string - empty string
    """
    email = ""
    password = ""
    first_name = ""
    last_name = ""
