from app import db
from app.models.base_model import BaseModel


class Amenity(BaseModel):
    """
    Amenity model representing features available in places.
    """

    __tablename__ = "amenities"

    name = db.Column(
        db.String(128),
        nullable=False,
        unique=True
    )

    description = db.Column(
        db.String(512),
        nullable=True
    )
