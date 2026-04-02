
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_jwt_extended import JWTManager
from flask_cors import CORS

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
    # Enable CORS for API endpoints (development)
    CORS(app, resources={r"/api/*": {"origins": "*"}})

    # Import and register blueprints
    from app.api.v1.auth import auth
    from app.api.v1.users import users
    # Blueprints adicionales (places, reviews, amenities)
    from app.api.v1.places import places
    from app.api.v1.reviews import reviews

    app.register_blueprint(auth, url_prefix="/api/v1")
    app.register_blueprint(users, url_prefix="/api/v1")
    app.register_blueprint(places, url_prefix="/api/v1")
    app.register_blueprint(reviews, url_prefix="/api/v1")

    # Amenities puede no estar implementado en esta copia; registrar si existe
    try:
        from app.api.v1.amenities import amenities
        app.register_blueprint(amenities, url_prefix="/api/v1")
    except Exception:
        # Ignorar si no está disponible
        pass

    # Simple healthcheck endpoint useful for docker/monitoring
    @app.route('/health', methods=['GET'])
    def health():
        return { 'status': 'ok' }, 200

    return app
