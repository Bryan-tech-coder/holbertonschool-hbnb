from app import db
from app.models.base_model import BaseModel

# Association table for many-to-many relationship
place_amenity = db.Table(
    "place_amenity",

    db.Column(
        "place_id",
        db.Integer,
        db.ForeignKey("places.id"),
        primary_key=True
    ),

    db.Column(
        "amenity_id",
        db.Integer,
        db.ForeignKey("amenities.id"),
        primary_key=True
    )
)


class Place(BaseModel):
    """
    Place model representing a place listed in HBnB.
    """

    __tablename__ = "places"

    name = db.Column(
        db.String(128),
        nullable=False
    )

    description = db.Column(
        db.String(1024),
        nullable=True
    )

    price = db.Column(
        db.Float,
        nullable=False
    )

    latitude = db.Column(
        db.Float,
        nullable=True
    )

    longitude = db.Column(
        db.Float,
        nullable=True
    )

    owner_id = db.Column(
        db.Integer,
        db.ForeignKey("users.id"),
        nullable=False
    )

    # Relationship: one place can have many reviews
    reviews = db.relationship(
        "Review",
        backref="place",
        cascade="all, delete-orphan"
    )

    # Relationship: many places can have many amenities
    amenities = db.relationship(
        "Amenity",
        secondary=place_amenity,
        backref="places"
    )
