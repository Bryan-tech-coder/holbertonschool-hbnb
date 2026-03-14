# app/api/v1/auth.py

from flask import Blueprint, request, jsonify
from flask_jwt_extended import create_access_token
from app.persistence.repository import UserRepository
from app.models.user import bcrypt

auth = Blueprint("auth", __name__)

repo = UserRepository()


@auth.route("/login", methods=["POST"])
def login():
    """
    Authenticate a user and return a JWT token.
    """

    data = request.get_json()

    if not data:
        return jsonify({"error": "Missing JSON"}), 400

    email = data.get("email")
    password = data.get("password")

    # Find user in database
    user = repo.get_user_by_email(email)

    # Validate credentials
    if not user or not bcrypt.check_password_hash(user.password, password):
        return jsonify({"error": "Invalid credentials"}), 401

    # Generate JWT token
    access_token = create_access_token(
        identity=user.id,
        additional_claims={"is_admin": user.is_admin}
    )

    return jsonify({"access_token": access_token}), 200
