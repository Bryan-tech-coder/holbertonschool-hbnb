from app import db
from app.models.user import User


class UserRepository:
    """
    Repository responsible for all database operations
    related to the User model.
    """

    def add(self, user):
        """
        Add a new user to the database.
        """
        db.session.add(user)
        db.session.commit()

    def save(self):
        """
        Commit changes already made to objects.
        """
        db.session.commit()

    def get_user_by_id(self, user_id):
        """
        Retrieve user by ID.
        """
        return User.query.get(user_id)

    def get_user_by_email(self, email):
        """
        Retrieve user by email.
        """
        return User.query.filter_by(email=email).first()
