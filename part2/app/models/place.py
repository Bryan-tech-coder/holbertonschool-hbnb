#!/usr/bin/python3
from app.models.base_model import BaseModel


class Place(BaseModel):
    def __init__(self, title, description, price, owner_id):
        super().__init__()

        if not title or not owner_id:
            raise ValueError("Place must have a title and owner")

        if price < 0:
            raise ValueError("Price must be positive")

        self.title = title
        self.description = description
        self.price = price
        self.owner_id = owner_id

        # Relationships
        self.reviews = []     # list of review IDs
        self.amenities = []   # list of amenity IDs
