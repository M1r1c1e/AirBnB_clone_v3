#!/usr/bin/python3
"""State handler"""
from flask import abort, jsonify, request
from api.v1.views import app_views
from models import storage
from models.state import State



@app_views.route("/states", methods=["GET", "POST"])
def get_states():
    """list of all states or creates a new state"""
    if request.method == "GET":
        states = [state.to_dict() for state in storage.all(State).values()]
        return jsonify(states)
    
    if request.method == "POST":
        request_data = request.get_json(silent=True)
        if not request_data:
            return jsonify({"error": "Not a JSON"}), 400
        if "name" not in request_data:
            return jsonify({"error": "Missing name"}), 400
        
        new_state = State(**request_data)
        new_state.save()
        return jsonify(new_state.to_dict()), 201


@app_views.route("/states/<state_id>", methods=["GET", "PUT", "DELETE"])
def get_state_by_id(state_id):
    """handles, updates, or deletes a state by its ID"""
    state = storage.get(State, state_id)
    if not state:
        abort(404)
    
    if request.method == "GET":
        return jsonify(state.to_dict())

    if request.method == "DELETE":
        state.delete()
        storage.save()
        return jsonify({}), 200

    if request.method == "PUT":
        request_data = request.get_json(silent=True)
        if not request_data:
            return jsonify({"error": "Not a JSON"}), 400

        # Update state object with the new data
        for key, value in request_data.items():
            if key not in ["id", "created_at", "updated_at"]:
                setattr(state, key, value)
        state.save()
        return jsonify(state.to_dict()), 200

