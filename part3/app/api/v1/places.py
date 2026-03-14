# app/api/v1/places.py
from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from app.models.place import Place
from app.persistence import repository

places = Blueprint("places", __name__)

# Crear lugar
@places.route("/places", methods=["POST"])
@jwt_required()
def create_place():
    current_user_id = get_jwt_identity()
    data = request.get_json()

    place = Place(
        name=data["name"],
        city_id=data["city_id"],
        user_id=current_user_id
    )

    repository.add(place)
    return jsonify(place.to_dict()), 201

# Actualizar lugar
@places.route("/places/<place_id>", methods=["PUT"])
@jwt_required()
def update_place(place_id):
    current_user_id = get_jwt_identity()
    place = repository.get_place_by_id(place_id)
    if not place:
        return jsonify({"error": "Place not found"}), 404
    if place.user_id != current_user_id:
        return jsonify({"error": "Unauthorized"}), 403

    data = request.get_json()
    for key in ["name", "description", "price"]:
        if key in data:
            setattr(place, key, data[key])

    repository.save()
    return jsonify(place.to_dict()), 200

# Borrar lugar
@places.route("/places/<place_id>", methods=["DELETE"])
@jwt_required()
def delete_place(place_id):
    current_user_id = get_jwt_identity()
    place = repository.get_place_by_id(place_id)
    if not place:
        return jsonify({"error": "Place not found"}), 404
    if place.user_id != current_user_id:
        return jsonify({"error": "Unauthorized"}), 403

    repository.delete(place)
    return jsonify({}), 204
