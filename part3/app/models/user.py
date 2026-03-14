from app import db
from app.models.base_model import BaseModel
from flask_bcrypt import Bcrypt

bcrypt = Bcrypt()


class User(BaseModel):
    """
    User model representing application users.
    """

    __tablename__ = "users"

    email = db.Column(
        db.String(128),
        unique=True,
        nullable=False
    )

    first_name = db.Column(
        db.String(128),
        nullable=False
    )

    last_name = db.Column(
        db.String(128),
        nullable=False
    )

    password = db.Column(
        db.String(128),
        nullable=False
    )

    is_admin = db.Column(
        db.Boolean,
        default=False
    )

    # Relationship: one user can own many places
    places = db.relationship(
        "Place",
        backref="owner",
        cascade="all, delete-orphan"
    )

    # Relationship: one user can write many reviews
    reviews = db.relationship(
        "Review",
        backref="author",
        cascade="all, delete-orphan"
    )
