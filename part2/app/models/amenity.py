#!/usr/bin/python3
from app.models.base_model import BaseModel


class Amenity(BaseModel):
    def __init__(self, name):
        super().__init__()

        if not name:
            raise ValueError("Amenity name cannot be empty")

        self.name = name
