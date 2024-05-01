#!/usr/bin/python3
"""
handling place operation
"""

from flask import jsonify, abort, request
from api.v1.views import app_views, storage
from models.place import Place
from models.user import User
from models.city import City

@app_views.route("/cities/<city_id>/places", methods=["GET"], strict_slashes=False)
def get_place_by_city(city_id):
    city = storage.get(City, city_id)
    if not city:
        abort(404)

    places = [place.to_dict() for place in city.places]
    return jsonify(places)

@app_views.route("/cities/<city_id>/places", methods=["POST"], strict_slashes=False)
def create_place(city_id):
    city = storage.get(City, city_id)
    if not city:
        abort(404)

    data = request.get_json(silent=True)
    if not data or "user_id" not in data or "name" not in data:
        abort(400, "Not a JSON" if not data else "Missing user_id or name")

    user_id = data.get("user_id")
    user = storage.get(User, user_id)
    if not user:
        abort(404)

    new_place = Place(city_id=city_id, **data)
    new_place.save()

    return jsonify(new_place.to_dict()), 201

@app_views.route("/places/<place_id>", methods=["GET"], strict_slashes=False)
def get_place_ID(place_id):
    place = storage.get(Place, place_id)
    if not place:
        abort(404)

    return jsonify(place.to_dict())

@app_views.route("/places/<place_id>", methods=["PUT"], strict_slashes=False)
def update_place(place_id):
    place = storage.get(Place, place_id)
    if not place:
        abort(404)

    data = request.get_json(silent=True)
    if not data:
        abort(400, "Not a JSON")

    for key, value in data.items():
        if key not in ["id", "user_id", "city_id", "created_at", "updated_at"]:
            setattr(place, key, value)

    place.save()
    return jsonify(place.to_dict()), 200

@app_views.route("/places/<place_id>", methods=["DELETE"], strict_slashes=False)
def delete_place(place_id):
    place = storage.get(Place, place_id)
    if not place:
        abort(404)

    storage.delete(place)
    storage.save()

    return jsonify({}), 200

