#!/usr/bin/python3
from app.models.base_model import BaseModel

class Amenity(BaseModel):
    def __init__(self, name):
        super().__init__()
        self.name = name

    def to_dict(self):
        base = super().to_dict()
        base.update({"name": self.name})
        return base
