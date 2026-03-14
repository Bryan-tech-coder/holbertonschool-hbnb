from app import db
from app.models.base_model import BaseModel


class Review(BaseModel):
    """
    Review model representing a user's review of a place.
    """

    __tablename__ = "reviews"

    text = db.Column(
        db.String(1024),
        nullable=False
    )

    rating = db.Column(
        db.Integer,
        nullable=False
    )

    user_id = db.Column(
        db.Integer,
        db.ForeignKey("users.id"),
        nullable=False
    )

    place_id = db.Column(
        db.Integer,
        db.ForeignKey("places.id"),
        nullable=False
    )
