# app/api/v1/users.py

from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity, get_jwt
from app.models.user import User, bcrypt
from app.persistence.repository import UserRepository

users = Blueprint("users", __name__)

repo = UserRepository()


def admin_required(fn):
    """
    Decorator used to restrict access to admin users.
    """
    from functools import wraps

    @wraps(fn)
    def wrapper(*args, **kwargs):

        claims = get_jwt()

        if not claims.get("is_admin"):
            return jsonify({"error": "Admin privileges required"}), 403

        return fn(*args, **kwargs)

    return wrapper


@users.route("/users", methods=["POST"])
def create_user():
    """
    Create a new user.
    """

    data = request.get_json()

    required = ["email", "first_name", "last_name", "password"]

    # Validate required fields
    for field in required:
        if field not in data:
            return jsonify({"error": f"{field} is required"}), 400

    # Prevent duplicate emails
    if repo.get_user_by_email(data["email"]):
        return jsonify({"error": "Email already exists"}), 400

    # Hash password
    hashed_password = bcrypt.generate_password_hash(
        data["password"]
    ).decode("utf-8")

    user = User(
        email=data["email"],
        first_name=data["first_name"],
        last_name=data["last_name"],
        password=hashed_password,
        is_admin=data.get("is_admin", False)
    )

    repo.add(user)

    return jsonify(user.to_dict()), 201


@users.route("/users/<int:user_id>", methods=["PUT"])
@jwt_required()
def update_user(user_id):
    """
    Update user information.

    Normal users:
    - can only update themselves

    Admin users:
    - can update anyone
    """

    current_user = get_jwt_identity()
    claims = get_jwt()

    data = request.get_json()

    user = repo.get_user_by_id(user_id)

    if not user:
        return jsonify({"error": "User not found"}), 404

    # Ownership check
    if current_user != user_id and not claims.get("is_admin"):
        return jsonify({"error": "Unauthorized"}), 403

    allowed_fields = [
        "first_name",
        "last_name",
        "email",
        "password",
        "is_admin"
    ]

    for field in allowed_fields:
        if field in data:

            if field == "password":
                hashed = bcrypt.generate_password_hash(
                    data["password"]
                ).decode("utf-8")

                setattr(user, field, hashed)

            else:
                setattr(user, field, data[field])

    repo.save()

    return jsonify(user.to_dict()), 200
