#!/usr/bin/python3
from flask import request
from flask_restx import Namespace, Resource, fields
from app.services.facade import HBnBFacade

api = Namespace(
    "amenities",
    path="/api/v1/amenities",
    description="Amenity operations"
)

facade = HBnBFacade()

amenity_model = api.model("Amenity", {
    "id": fields.String(readonly=True),
    "name": fields.String(required=True),
    "created_at": fields.DateTime,
    "updated_at": fields.DateTime
})

@api.route("/")
class AmenityList(Resource):
    @api.expect(amenity_model, validate=True)
    @api.marshal_with(amenity_model, code=201)
    def post(self):
        data = request.json
        amenity = facade.create_amenity(data)
        return amenity, 201

    @api.marshal_list_with(amenity_model)
    def get(self):
        return facade.get_all_amenities()

@api.route("/<string:amenity_id>")
class AmenityResource(Resource):
    @api.marshal_with(amenity_model)
    def get(self, amenity_id):
        amenity = facade.get_amenity(amenity_id)
        if not amenity:
            api.abort(404, "Amenity not found")
        return amenity

    @api.expect(amenity_model, validate=True)
    @api.marshal_with(amenity_model)
    def put(self, amenity_id):
        data = request.json
        updated = facade.update_amenity(amenity_id, data)
        if not updated:
            api.abort(404, "Amenity not found")
        return updated
