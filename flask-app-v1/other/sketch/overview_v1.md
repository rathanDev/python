# Project Structure
# flask_app/
# ├── app/
# │   ├── __init__.py
# │   ├── config.py
# │   ├── extensions.py
# │   ├── models.py
# │   ├── schemas.py
# │   ├── services/
# │   │   └── user_service.py
# │   ├── routes/
# │   │   └── user_routes.py
# │   └── logging_config.py
# ├── run.py
# ├── pyproject.toml
# └── .env

# ======================= pyproject.toml =======================
# Use UV: uv venv && uv pip install -r requirements.txt

[project]
name = "flask-crud-app"
version = "0.1.0"
dependencies = [
    "flask",
    "flask-sqlalchemy",
    "pydantic",
    "python-dotenv"
]

# ======================= .env =======================
FLASK_ENV=development
DATABASE_URL=sqlite:///app.db

# ======================= app/config.py =======================
import os

class Config:
    SQLALCHEMY_DATABASE_URI = os.getenv("DATABASE_URL")
    SQLALCHEMY_TRACK_MODIFICATIONS = False

class DevelopmentConfig(Config):
    DEBUG = True

class ProductionConfig(Config):
    DEBUG = False

config_map = {
    "development": DevelopmentConfig,
    "production": ProductionConfig
}

# ======================= app/extensions.py =======================
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

# ======================= app/models.py =======================
from .extensions import db

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)

# ======================= app/schemas.py =======================
from pydantic import BaseModel, EmailStr

class UserCreate(BaseModel):
    name: str
    email: EmailStr

class UserResponse(BaseModel):
    id: int
    name: str
    email: EmailStr

# ======================= app/services/user_service.py =======================
from app.models import User
from app.extensions import db

class UserService:
    def create_user(self, data):
        user = User(**data)
        db.session.add(user)
        db.session.commit()
        return user

    def get_all_users(self):
        return User.query.all()

    def get_user(self, user_id):
        return User.query.get(user_id)

    def update_user(self, user_id, data):
        user = self.get_user(user_id)
        if not user:
            return None
        for key, value in data.items():
            setattr(user, key, value)
        db.session.commit()
        return user

    def delete_user(self, user_id):
        user = self.get_user(user_id)
        if not user:
            return False
        db.session.delete(user)
        db.session.commit()
        return True

# ======================= app/routes/user_routes.py =======================
from flask import Blueprint, request, jsonify
from app.services.user_service import UserService
from app.schemas import UserCreate

user_bp = Blueprint("users", __name__)
service = UserService()  # Simple DI

@user_bp.route("/users", methods=["POST"])
def create_user():
    data = request.get_json()
    validated = UserCreate(**data)
    user = service.create_user(validated.dict())
    return jsonify({"id": user.id, "name": user.name, "email": user.email}), 201

@user_bp.route("/users", methods=["GET"])
def get_users():
    users = service.get_all_users()
    return jsonify([{"id": u.id, "name": u.name, "email": u.email} for u in users])

@user_bp.route("/users/<int:user_id>", methods=["GET"])
def get_user(user_id):
    user = service.get_user(user_id)
    if not user:
        return jsonify({"error": "Not found"}), 404
    return jsonify({"id": user.id, "name": user.name, "email": user.email})

@user_bp.route("/users/<int:user_id>", methods=["PUT"])
def update_user(user_id):
    data = request.get_json()
    user = service.update_user(user_id, data)
    if not user:
        return jsonify({"error": "Not found"}), 404
    return jsonify({"id": user.id, "name": user.name, "email": user.email})

@user_bp.route("/users/<int:user_id>", methods=["DELETE"])
def delete_user(user_id):
    success = service.delete_user(user_id)
    if not success:
        return jsonify({"error": "Not found"}), 404
    return jsonify({"message": "Deleted"})

# ======================= app/logging_config.py =======================
import logging

def setup_logging():
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s - %(levelname)s - %(message)s"
    )

# ======================= app/__init__.py =======================
from flask import Flask
from .config import config_map
from .extensions import db
from .routes.user_routes import user_bp
from .logging_config import setup_logging
import os


def create_app():
    env = os.getenv("FLASK_ENV", "development")
    app = Flask(__name__)

    app.config.from_object(config_map[env])

    setup_logging()
    db.init_app(app)

    app.register_blueprint(user_bp)

    with app.app_context():
        db.create_all()

    return app

# ======================= run.py =======================
from app import create_app

app = create_app()

if __name__ == "__main__":
    app.run()
