# app/api/v1/reviews.py
from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from app.models.review import Review
from app.persistence import repository

reviews = Blueprint("reviews", __name__)

# Crear review
@reviews.route("/reviews", methods=["POST"])
@jwt_required()
def create_review():
    current_user_id = get_jwt_identity()
    data = request.get_json()
    place = repository.get_place_by_id(data["place_id"])

    if not place:
        return jsonify({"error": "Place not found"}), 404
    if place.user_id == current_user_id:
        return jsonify({"error": "Cannot review your own place"}), 403

    existing_review = repository.get_review_by_user_place(current_user_id, place.id)
    if existing_review:
        return jsonify({"error": "You already reviewed this place"}), 403

    review = Review(
      text=data["text"],
      user_id=current_user_id,
      place_id=data["place_id"]
)

    repository.add(review)
    return jsonify(review.to_dict()), 201

# Actualizar review
@reviews.route("/reviews/<review_id>", methods=["PUT"])
@jwt_required()
def update_review(review_id):
    current_user_id = get_jwt_identity()
    review = repository.get_review_by_id(review_id)

    if not review:
        return jsonify({"error": "Review not found"}), 404
    if review.user_id != current_user_id:
        return jsonify({"error": "Unauthorized"}), 403

    data = request.get_json()
    if "text" in data:
        review.text = data["text"]

    repository.save()
    return jsonify(review.to_dict()), 200
