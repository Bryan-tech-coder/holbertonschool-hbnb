#!/usr/bin/python3
from flask import request
from flask_restx import Namespace, Resource, fields
from app.services.facade import HBnBFacade

api = Namespace(
    "places",
    path="/api/v1/places",
    description="Place operations"
)

facade = HBnBFacade()

place_model = api.model("Place", {
    "id": fields.String(readonly=True),
    "name": fields.String(required=True),
    "description": fields.String,
    "number_rooms": fields.Integer,
    "number_bathrooms": fields.Integer,
    "max_guest": fields.Integer,
    "price_by_night": fields.Float(required=True),
    "latitude": fields.Float(required=True),
    "longitude": fields.Float(required=True),
    "owner_id": fields.String(required=True),
    "amenity_ids": fields.List(fields.String),
    "review_ids": fields.List(fields.String),
    "created_at": fields.DateTime,
    "updated_at": fields.DateTime
})

@api.route("/")
class PlaceList(Resource):
    @api.expect(place_model, validate=True)
    @api.marshal_with(place_model, code=201)
    def post(self):
        data = request.json
        place = facade.create_place(data)
        if not place:
            api.abort(400, "Owner not found")
        return place, 201

    @api.marshal_list_with(place_model)
    def get(self):
        return facade.get_all_places()

@api.route("/<string:place_id>")
class PlaceResource(Resource):
    @api.marshal_with(place_model)
    def get(self, place_id):
        place = facade.get_place(place_id)
        if not place:
            api.abort(404, "Place not found")
        return place

    @api.expect(place_model, validate=True)
    @api.marshal_with(place_model)
    def put(self, place_id):
        data = request.json
        updated_place = facade.update_place(place_id, data)
        if not updated_place:
            api.abort(404, "Place not found")
        return updated_place
