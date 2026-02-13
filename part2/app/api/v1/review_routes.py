#!/usr/bin/python3
from flask import request
from flask_restx import Namespace, Resource, fields
from app.services.facade import HBnBFacade

api = Namespace(
    "reviews",
    path="/api/v1/reviews",
    description="Review operations"
)

facade = HBnBFacade()

# Swagger model
review_model = api.model("Review", {
    "id": fields.String(readonly=True),
    "user_id": fields.String(required=True),
    "place_id": fields.String(required=True),
    "text": fields.String(required=True),
    "created_at": fields.DateTime,
    "updated_at": fields.DateTime
})

# ---------- POST / GET ----------
@api.route("/")
class ReviewList(Resource):
    @api.expect(review_model, validate=True)
    @api.marshal_with(review_model, code=201)
    def post(self):
        data = request.json
        review = facade.create_review(data)
        if not review:
            api.abort(400, "Invalid user, place, or empty text")
        return review, 201

    @api.marshal_list_with(review_model)
    def get(self):
        return facade.get_all_reviews()

# ---------- GET / PUT / DELETE by ID ----------
@api.route("/<string:review_id>")
class ReviewResource(Resource):
    @api.marshal_with(review_model)
    def get(self, review_id):
        review = facade.get_review(review_id)
        if not review:
            api.abort(404, "Review not found")
        return review

    @api.expect(review_model, validate=True)
    @api.marshal_with(review_model)
    def put(self, review_id):
        data = request.json
        review = facade.update_review(review_id, data)
        if not review:
            api.abort(404, "Review not found")
        return review

    def delete(self, review_id):
        review = facade.delete_review(review_id)
        if not review:
            api.abort(404, "Review not found")
        return {"message": "Review deleted successfully"}, 200
