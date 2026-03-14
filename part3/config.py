class Config:
    """
    Configuration class used by Flask.
    Stores settings for JWT and database.
    """

    SECRET_KEY = "super-secret-key"

    # JWT configuration
    JWT_SECRET_KEY = "jwt-secret-string"

    # SQLite database for development
    SQLALCHEMY_DATABASE_URI = "sqlite:///hbnb.db"

    # Disable modification tracking (improves performance)
    SQLALCHEMY_TRACK_MODIFICATIONS = False
