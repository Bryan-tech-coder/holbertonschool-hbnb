from app import db
from app.models.user import User
from app.models.place import Place
from app.models.review import Review
from app.models.amenity import Amenity


class UserRepository:
    def add(self, obj):
        db.session.add(obj)
        db.session.commit()

    def save(self):
        db.session.commit()

    def delete(self, obj):
        db.session.delete(obj)
        db.session.commit()

    # ================= USERS =================
    def get_user_by_id(self, user_id):
        return User.query.get(user_id)

    def get_user_by_email(self, email):
        return User.query.filter_by(email=email).first()

    # ================= PLACES =================
    def get_all_places(self):
        return Place.query.all()

    def get_place_by_id(self, place_id):
        return Place.query.get(place_id)

    # ================= REVIEWS =================
    def get_review_by_id(self, review_id):
        return Review.query.get(review_id)

    def get_review_by_user_place(self, user_id, place_id):
        return Review.query.filter_by(
            user_id=user_id,
            place_id=place_id
        ).first()

    # ================= AMENITIES =================
    def get_all_amenities(self):
        return Amenity.query.all()
