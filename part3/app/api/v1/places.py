from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from app.models.place import Place
from app.persistence.repository import UserRepository

places = Blueprint("places", __name__)
repo = UserRepository()


# ================= GET ALL PLACES =================
@places.route("/places", methods=["GET"])
def get_places():
    all_places = repo.get_all_places()

    result = []
    for p in all_places:
        data = p.to_dict()

        # owner
        data["owner"] = {
            "id": p.owner.id,
            "email": p.owner.email
        } if p.owner else None

        # amenities
        data["amenities"] = [
            {"id": a.id, "name": a.name}
            for a in p.amenities
        ]

        # reviews (solo básicos aquí)
        data["reviews"] = [
            {"id": r.id, "text": r.text}
            for r in p.reviews
        ]

        result.append(data)

    return jsonify(result), 200


# ================= GET ONE PLACE =================
@places.route("/places/<int:place_id>", methods=["GET"])
def get_place(place_id):
    p = repo.get_place_by_id(place_id)

    if not p:
        return jsonify({"error": "Place not found"}), 404

    data = p.to_dict()

    data["owner"] = {
        "id": p.owner.id,
        "email": p.owner.email
    } if p.owner else None

    data["amenities"] = [
        {"id": a.id, "name": a.name}
        for a in p.amenities
    ]

    data["reviews"] = [
        {
            "id": r.id,
            "text": r.text,
            "user_id": r.user_id
        }
        for r in p.reviews
    ]

    return jsonify(data), 200


# ================= CREATE PLACE =================
@places.route("/places", methods=["POST"])
@jwt_required()
def create_place():
    current_user_id = get_jwt_identity()
    data = request.get_json()

    place = Place(
        name=data["name"],
        description=data.get("description"),
        price=data.get("price", 0),
        owner_id=current_user_id
    )

    repo.add(place)
    return jsonify(place.to_dict()), 201


# ================= UPDATE PLACE =================
@places.route("/places/<int:place_id>", methods=["PUT"])
@jwt_required()
def update_place(place_id):
    current_user_id = get_jwt_identity()
    place = repo.get_place_by_id(place_id)

    if not place:
        return jsonify({"error": "Place not found"}), 404

    if place.owner_id != current_user_id:
        return jsonify({"error": "Unauthorized"}), 403

    data = request.get_json()

    for field in ["name", "description", "price"]:
        if field in data:
            setattr(place, field, data[field])

    repo.save()
    return jsonify(place.to_dict()), 200


# ================= DELETE PLACE =================
@places.route("/places/<int:place_id>", methods=["DELETE"])
@jwt_required()
def delete_place(place_id):
    current_user_id = get_jwt_identity()
    place = repo.get_place_by_id(place_id)

    if not place:
        return jsonify({"error": "Place not found"}), 404

    if place.owner_id != current_user_id:
        return jsonify({"error": "Unauthorized"}), 403

    repo.delete(place)
    return jsonify({}), 204
