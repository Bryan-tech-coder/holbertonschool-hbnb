#!/usr/bin/python3
"""
Facade for HBnB services
"""

from app.persistence.repository import InMemoryRepository
from app.models.user import User
from app.models.place import Place
from app.models.amenity import Amenity


class HBnBFacade:
    def __init__(self):
        # Repositorios en memoria
        self.user_repo = InMemoryRepository()
        self.place_repo = InMemoryRepository()
        self.amenity_repo = InMemoryRepository()

    # ---------- USERS ----------
    def create_user(self, data):
        user = User(
            first_name=data.get("first_name"),
            last_name=data.get("last_name"),
            email=data.get("email")
        )
        self.user_repo.add(user)
        return user

    def get_user(self, user_id):
        return self.user_repo.get(user_id)

    def get_all_users(self):
        return self.user_repo.get_all()

    def update_user(self, user_id, data):
        return self.user_repo.update(user_id, data)

    # ---------- AMENITIES ----------
    def create_amenity(self, data):
        amenity = Amenity(name=data.get("name"))
        self.amenity_repo.add(amenity)
        return amenity

    def get_amenity(self, amenity_id):
        return self.amenity_repo.get(amenity_id)

    def get_all_amenities(self):
        return self.amenity_repo.get_all()

    def update_amenity(self, amenity_id, data):
        return self.amenity_repo.update(amenity_id, data)

    # ---------- PLACES ----------
    def create_place(self, data):
        owner_id = data.get("owner_id")
        owner = self.user_repo.get(owner_id)
        if not owner:
            return None  # Owner no existe

        place = Place(
            name=data.get("name"),
            description=data.get("description"),
            number_rooms=data.get("number_rooms"),
            number_bathrooms=data.get("number_bathrooms"),
            max_guest=data.get("max_guest"),
            price_by_night=data.get("price_by_night"),
            latitude=data.get("latitude"),
            longitude=data.get("longitude"),
            owner_id=owner_id,
            amenities=data.get("amenities", [])  # lista de IDs
        )
        self.place_repo.add(place)
        return place

    def get_place(self, place_id):
        return self.place_repo.get(place_id)

    def get_all_places(self):
        return self.place_repo.get_all()

    def update_place(self, place_id, data):
        return self.place_repo.update(place_id, data)
