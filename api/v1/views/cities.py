#!/usr/bin/python3
"""City handler"""
from flask import abort, jsonify, request
from api.v1.views import app_views
from models import storage
from models.city import City
from models.state import State


@app_views.route("/states/<state_id>/cities", methods=["GET", "POST"])
def state_cities(state_id=None):
    """list of all cities of a state or creates a new city"""
    # Checking if state exists
    state = storage.get(State, state_id)
    if not state:
        abort(404)

    if request.method == "GET":
        cities = [city.to_dict() for city in state.cities]
        return jsonify(cities)

    if request.method == "POST":
        request_data = request.get_json(silent=True)
        if not request_data:
            return jsonify({"error": "Not a JSON"}), 400
        if "name" not in request_data:
            return jsonify({"error": "Missing name"}), 400

        new_city = City(state_id=state_id, **request_data)
        new_city.save()
        return jsonify(new_city.to_dict()), 201


@app_views.route("/cities/<city_id>", methods=["GET", "PUT", "DELETE"])
def get_city_by_id(city_id):
    """Listingupdates, or deletes a city by its ID"""
    city = storage.get(City, city_id)
    if not city:
        abort(404)

    if request.method == "GET":
        return jsonify(city.to_dict())

    if request.method == "DELETE":
        city.delete()
        storage.save()
        return jsonify({}), 200

    if request.method == "PUT":
        request_data = request.get_json(silent=True)
        if not request_data:
            return jsonify({"error": "Not a JSON"}), 400

        # Update city list with the new data
        for key, value in request_data.items():
            if key not in ["id", "state_id", "created_at", "updated_at"]:
                setattr(city, key, value)
        city.save()
        return jsonify(city.to_dict()), 200

