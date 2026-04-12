from flask import Blueprint, request, jsonify 
from app.services.user_service import UserService
from app.schemas import UserCreate

user_bp = Blueprint("users", __name__)
service = UserService()

@user_bp.route("/users", methods=["POST"])
def create_user():
    data = request.get_json()
    validated = UserCreate(**data)
    user = service.create_user(validated.dict())
    return jsonify({"id":user.id, "name":user.name, "email":user.email}), 201

@user_bp.route("/users", methods=["GET"])
def create_user
