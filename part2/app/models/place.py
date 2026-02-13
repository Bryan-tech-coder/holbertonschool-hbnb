#!/usr/bin/python3
from app.models.base_model import BaseModel  


class Place(BaseModel):
    def __init__(self, name, owner_id, description="", number_rooms=0,
                 number_bathrooms=0, max_guest=0, price_by_night=0.0,
                 latitude=0.0, longitude=0.0, amenity_ids=None):
        super().__init__()
        if not name or not owner_id:
            raise ValueError("Place must have a name and owner")
        if price_by_night < 0:
            raise ValueError("Price must be positive")

        self.name = name
        self.description = description
        self.number_rooms = number_rooms
        self.number_bathrooms = number_bathrooms
        self.max_guest = max_guest
        self.price_by_night = price_by_night
        self.latitude = latitude
        self.longitude = longitude
        self.owner_id = owner_id
        self.amenity_ids = amenity_ids or []
        self.review_ids = []  # <--- Aquí

    def to_dict(self):
        base = super().to_dict()
        base.update({
            "name": self.name,
            "description": self.description,
            "number_rooms": self.number_rooms,
            "number_bathrooms": self.number_bathrooms,
            "max_guest": self.max_guest,
            "price_by_night": self.price_by_night,
            "latitude": self.latitude,
            "longitude": self.longitude,
            "owner_id": self.owner_id,
            "amenity_ids": self.amenity_ids,
            "review_ids": self.review_ids
        })
        return base
