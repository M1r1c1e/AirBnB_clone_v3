#!/usr/bin/python3
"""The API index code"""
from flask import jsonify
from api.v1.views import app_views


@app_views.route('/status', methods=['GET'], strict_slashes=False)
def status():
    return jsonify({"status": "OK"})

@app_views.route("/stats", methods=['GET'], strict_slashes=False)
def stats():
    """gets number of objects"""
    obj_count = {
            'amenities': storage.count('Amenity'),
            'cities': storage.count('City'),
            'places': storage.count('Place'),
            'reviews': storage.count('Review'),
            'states': storage.count('State'),
            'users': storage.count('User')
    }
    return jsonify(obj_count)
