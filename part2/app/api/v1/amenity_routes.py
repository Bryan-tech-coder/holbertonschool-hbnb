#!/usr/bin/python3
from flask import request
from flask_restx import Namespace, Resource, fields
from app.services.facade import HBnBFacade

# Namespace
api = Namespace(
    "amenities",
    path="/api/v1/amenities",
    description="Amenity operations"
)

facade = HBnBFacade()

# Amenity Model
amenity_model = api.model("Amenity", {
    "id": fields.String(readonly=True),
    "name": fields.String(required=True),
    "created_at": fields.DateTime,
    "updated_at": fields.DateTime
})

# POST / GET list
@api.route("/")
class AmenityList(Resource):

    @api.expect(amenity_model, validate=True)
    @api.marshal_with(amenity_model, code=201)
    def post(self):
        """Create a new amenity"""
        data = request.json
        amenity = facade.create_amenity(data)
        return amenity, 201

    @api.marshal_list_with(amenity_model)
    def get(self):
        """Retrieve all amenities"""
        return facade.get_all_amenities()

# GET / PUT by id
@api.route("/<string:amenity_id>")
class AmenityResource(Resource):

    @api.marshal_with(amenity_model)
    def get(self, amenity_id):
        """Retrieve an amenity by ID"""
        amenity = facade.get_amenity(amenity_id)
        if not amenity:
            api.abort(404, "Amenity not found")
        return amenity

    @api.expect(amenity_model, validate=True)
    @api.marshal_with(amenity_model)
    def put(self, amenity_id):
        """Update an amenity"""
        data = request.json
        amenity = facade.update_amenity(amenity_id, data)
        if not amenity:
            api.abort(404, "Amenity not found")
        return amenity
