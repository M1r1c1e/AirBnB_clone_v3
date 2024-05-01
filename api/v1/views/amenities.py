#!/usr/bin/python3
"""
handling amenity object and operations
"""
from flask import jsonify, abort, request
from api.v1.views import app_views, storage
from models.amenity import Amenity


@app_views.route("/amenities", methods=["GET"], strict_slashes=False)
def getall_amenity():
    amenities = []
    am_obj = storage.all("Amenity")
    for item in am_obj.values():
        amenities.append(item.to_json())

    return jsonify(amenities)


@app_views.route("/amenities", methods=["POST"], strict_slashes=False)
def amenity_create:
    data = request.get_json(silent=True)
    if not data or "name" not in data:
        abort(400, "Not a JSON" if not data else "Missing name")

    new_amenity = Amenity(**data)
    new_amenity.save()

    return jsonify(amenity.to_json()), 201


@app_views.route("/amenities/<amenity_id>",  methods=["GET"],
                 strict_slashes=False)
def amenity_by_id(amenity_id):
    amenity = storage.get(Amenity, amenity_id)
    if not amenity:
        abort(404)
    return jsonify(amenity.to_json())


@app_views.route("/amenities/<amenity_id>",  methods=["PUT"],
                 strict_slashes=False)
def amenity_updateMe(amenity_id):
    data_json = request.get_json(silent=True)
    if not data_json:
        abort(400, "Not a JSON")

    amenity = storage.get(Amenity, amenity_id)
    if not amenity:
        abort(404)

    for key, value in data_json.items():
        if key not in ["id", "created_at", "updated_at"]:
            setattr(amenity, key, value)

    amenity.save()
    return jsonify(amenity.to_json()), 200


@app_views.route("/amenities/<amenity_id>",  methods=["DELETE"],
                 strict_slashes=False)
def amenity_delete_by_id(amenity_id):
    """
    deleting amenity identified by ID
    """
    amenity = storage.get("Amenity", str(amenity_id))

    if amenity is None:
        abort(404)

    storage.delete(amenity)
    storage.save()

    return jsonify({}), 200
