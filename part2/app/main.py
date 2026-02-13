#!/usr/bin/python3
from flask import Flask
from flask_restx import Api
from app.api.v1.routes import api as users_api
from app.api.v1.place_routes import api as places_api
from app.api.v1.amenity_routes import api as amenities_api

def create_app():
    app = Flask(__name__)
    api = Api(app, title="HBnB API", version="1.0")

    # Registrar namespaces
    api.add_namespace(users_api)
    api.add_namespace(places_api)
    api.add_namespace(amenities_api)

    return app

if __name__ == "__main__":
    app = create_app()
    app.run(debug=True)
