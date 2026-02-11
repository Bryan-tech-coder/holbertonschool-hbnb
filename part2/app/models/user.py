#!/usr/bin/python3
from app.models.base_model import BaseModel


class User(BaseModel):
    def __init__(self, first_name, last_name, email):
        super().__init__()

        if not first_name or not last_name or not email:
            raise ValueError("User attributes cannot be empty")

        self.first_name = first_name
        self.last_name = last_name
        self.email = email

        # Relationships
        self.places = []    # list of place IDs
        self.reviews = []   # list of review IDs
