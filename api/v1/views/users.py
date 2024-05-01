#!/usr/bin/python3
"""
Handling User objects and operations
"""
from flask import jsonify, abort, request
from api.v1.views import app_views, storage
from models.user import User

@app_views.route("/amenities", methods=["GET"], strict_slashes=False)
def getall_user():
    users = []
    user_obj = storage.all("Amenity")
    for item in am_obj.values():
        users.append(item.to_json())

    return jsonify(users)

@app_views.route("/users", methods=["POST"], strict_slashes=False)
def create_user():
    data = request.get_json(silent=True)
    if not data or "email" not in data or "password" not in data:
        abort(400, "Not a JSON" if not data else "Missing email or password")

    user = User(**data)
    user.save()

    return jsonify(user.to_dict()), 201

@app_views.route("/users/<user_id>", methods=["GET"], strict_slashes=False)
def get_user(user_id):
    user = storage.get(User, user_id)
    if not user:
        abort(404)
    return jsonify(user.to_dict())

@app_views.route("/users/<user_id>", methods=["PUT"], strict_slashes=False)
def update_user(user_id):
    data = request.get_json(silent=True)
    if not data:
        abort(400, "Not a JSON")

    user = storage.get(User, user_id)
    if not user:
        abort(404)

    for key, value in data.items():
        if key not in ["id", "email", "created_at", "updated_at", "password"]:
            setattr(user, key, value)

    user.save()
    return jsonify(user.to_dict()), 200

@app_views.route("/users/<user_id>", methods=["DELETE"], strict_slashes=False)
def delete_user(user_id):
    user = storage.get(User, user_id)
    if not user:
        abort(404)

    storage.delete(user)
    storage.save()

    return jsonify({}), 200

