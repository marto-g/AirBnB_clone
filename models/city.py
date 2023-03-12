#!/usr/bin/python3
"""
defines City class that inherits from BaseModel class
"""
from models.base_model import BaseModel


class City(BaseModel):
    """
    Attr:
    state_id: string - empty string: it will be the State.id
    name: string - empty string
    """
    state_id = ""
    name = ""
