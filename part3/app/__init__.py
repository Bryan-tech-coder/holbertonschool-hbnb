
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_jwt_extended import JWTManager

# SQLAlchemy instance (used in models)
db = SQLAlchemy()

# JWT instance
jwt = JWTManager()


def create_app(config_class):
    """
    Application Factory pattern.
    Creates and configures the Flask application.
    """

    app = Flask(__name__)

    # Load configuration
    app.config.from_object(config_class)

    # Initialize extensions
    db.init_app(app)
    jwt.init_app(app)

    # Import and register blueprints
    from app.api.v1.auth import auth
    from app.api.v1.users import users

    app.register_blueprint(auth, url_prefix="/api/v1")
    app.register_blueprint(users, url_prefix="/api/v1")

    return app
