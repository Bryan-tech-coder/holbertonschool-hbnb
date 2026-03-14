from datetime import datetime
from app import db


class BaseModel(db.Model):
    """
    BaseModel is an abstract class that provides
    common attributes for all models.
    """

    __abstract__ = True  # prevents SQLAlchemy from creating a table

    # Unique identifier for every object
    id = db.Column(db.Integer, primary_key=True)

    # Timestamp when object is created
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    # Timestamp updated automatically
    updated_at = db.Column(
        db.DateTime,
        default=datetime.utcnow,
        onupdate=datetime.utcnow
    )

    def to_dict(self):
        """
        Convert model object to dictionary.
        Useful when returning JSON responses.
        """
        return {c.name: getattr(self, c.name) for c in self.__table__.columns}
