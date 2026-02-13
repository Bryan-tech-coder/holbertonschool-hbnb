#!/usr/bin/python3
from flask import request
from flask_restx import Namespace, Resource, fields
from app.services.facade import HBnBFacade

api = Namespace(
    "users",
    path="/api/v1/users",
    description="User operations"
)

facade = HBnBFacade()

user_model = api.model("User", {
    "id": fields.String(readonly=True),
    "first_name": fields.String(required=True),
    "last_name": fields.String(required=True),
    "email": fields.String(required=True),
    "created_at": fields.DateTime,
    "updated_at": fields.DateTime
})

@api.route("/")
class UserList(Resource):
    @api.expect(user_model, validate=True)
    @api.marshal_with(user_model, code=201)
    def post(self):
        data = request.json
        user = facade.create_user(data)
        return user, 201

    @api.marshal_list_with(user_model)
    def get(self):
        return facade.get_all_users()

@api.route("/<string:user_id>")
class UserResource(Resource):
    @api.marshal_with(user_model)
    def get(self, user_id):
        user = facade.get_user(user_id)
        if not user:
            api.abort(404, "User not found")
        return user

    @api.expect(user_model, validate=True)
    @api.marshal_with(user_model)
    def put(self, user_id):
        data = request.json
        user = facade.update_user(user_id, data)
        if not user:
            api.abort(404, "User not found")
        return user
