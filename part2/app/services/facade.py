#!/usr/bin/python3
#!/usr/bin/python3
from app.persistence.repository import InMemoryRepository
from app.models.user import User
from app.models.place import Place
from app.models.amenity import Amenity
from app.models.review import Review

class HBnBFacade:
    def __init__(self):
        self.user_repo = InMemoryRepository()
        self.place_repo = InMemoryRepository()
        self.amenity_repo = InMemoryRepository()
        self.review_repo = InMemoryRepository()

    # ---------- USERS ----------
    def create_user(self, data):
        user = User(
            first_name=data.get("first_name"),
            last_name=data.get("last_name"),
            email=data.get("email")
        )
        self.user_repo.add(user)
        return user.to_dict()

    def get_user(self, user_id):
        user = self.user_repo.get(user_id)
        return user.to_dict() if user else None

    def get_all_users(self):
        return [u.to_dict() for u in self.user_repo.get_all()]

    def update_user(self, user_id, data):
        user = self.user_repo.update(user_id, data)
        return user.to_dict() if user else None

    # ---------- AMENITIES ----------
    def create_amenity(self, data):
        amenity = Amenity(name=data.get("name"))
        self.amenity_repo.add(amenity)
        return amenity.to_dict()

    def get_amenity(self, amenity_id):
        amenity = self.amenity_repo.get(amenity_id)
        return amenity.to_dict() if amenity else None

    def get_all_amenities(self):
        return [a.to_dict() for a in self.amenity_repo.get_all()]

    def update_amenity(self, amenity_id, data):
        amenity = self.amenity_repo.update(amenity_id, data)
        return amenity.to_dict() if amenity else None

    # ---------- PLACES ----------
    def create_place(self, data):
        owner = self.user_repo.get(data.get("owner_id"))
        if not owner:
            return None
        place = Place(
            name=data.get("name"),
            description=data.get("description", ""),
            number_rooms=data.get("number_rooms", 0),
            number_bathrooms=data.get("number_bathrooms", 0),
            max_guest=data.get("max_guest", 0),
            price_by_night=data.get("price_by_night", 0),
            latitude=data.get("latitude", 0),
            longitude=data.get("longitude", 0),
            owner_id=data.get("owner_id"),
            amenity_ids=data.get("amenity_ids", [])
        )
        self.place_repo.add(place)
        return place.to_dict()

    def get_place(self, place_id):
        place = self.place_repo.get(place_id)
        return place.to_dict() if place else None

    def get_all_places(self):
        return [p.to_dict() for p in self.place_repo.get_all()]

    def update_place(self, place_id, data):
        place = self.place_repo.update(place_id, data)
        return place.to_dict() if place else None

# ---------- REVIEWS ----------
def create_review(self, data):
    user = self.user_repo.get(data.get("user_id"))
    place = self.place_repo.get(data.get("place_id"))
    text = data.get("text", "").strip()
    if not user or not place or not text:
        return None
    review = Review(user_id=user.id, place_id=place.id, text=text)
    self.review_repo.add(review)
    place.review_ids.append(review.id)
    return review.to_dict()

def get_review(self, review_id):
    review = self.review_repo.get(review_id)
    return review.to_dict() if review else None

def get_all_reviews(self):
    return [r.to_dict() for r in self.review_repo.get_all()]

def update_review(self, review_id, data):
    review = self.review_repo.update(review_id, data)
    return review.to_dict() if review else None

def delete_review(self, review_id):
    review = self.review_repo.get(review_id)
    if not review:
        return None
    # remover review de place
    place = self.place_repo.get(review.place_id)
    if place and review_id in place.review_ids:
        place.review_ids.remove(review_id)
    self.review_repo.delete(review_id)
    return review.to_dict()
