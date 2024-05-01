#!/usr/bin/python3
"""
place review operations handler
"""
from flask import jsonify, abort, request
from api.v1.views import app_views, storage
from models.review import Review
from models.place import Place
from models.user import User

@app_views.route("/places/<place_id>/reviews", methods=["GET"], strict_slashes=False)
def get_reviews_by_place(place_id):
    place = storage.get(Place, place_id)
    if not place:
        abort(404)

    reviews = [review.to_dict() for review in place.reviews]
    return jsonify(reviews)

@app_views.route("/reviews/<review_id>", methods=["GET"], strict_slashes=False)
def get_review_ID(review_id):
    review = storage.get(Review, review_id)
    if not review:
        abort(404)

    return jsonify(review.to_dict())

@app_views.route("/reviews/<review_id>", methods=["DELETE"], strict_slashes=False)
def delete_review(review_id):
    review = storage.get(Review, review_id)
    if not review:
        abort(404)

    storage.delete(review)
    storage.save()

    return jsonify({}), 200

@app_views.route("/places/<place_id>/reviews", methods=["POST"], strict_slashes=False)
def create_review(place_id):
    place = storage.get(Place, place_id)
    if not place:
        abort(404)

    data = request.get_json(silent=True)
    if not data or "user_id" not in data or "text" not in data:
        abort(400, "Not a JSON" if not data else "Missing user_id or text")

    user_id = data.get("user_id")
    user = storage.get(User, user_id)
    if not user:
        abort(404)

    new_review = Review(place_id=place_id, **data)
    new_review.save()

    return jsonify(new_review.to_dict()), 201

@app_views.route("/reviews/<review_id>", methods=["PUT"], strict_slashes=False)
def update_review(review_id):
    review = storage.get(Review, review_id)
    if not review:
        abort(404)

    data = request.get_json(silent=True)
    if not data:
        abort(400, "Not a JSON")

    for key, value in data.items():
        if key not in ["id", "user_id", "place_id", "created_at", "updated_at"]:
            setattr(review, key, value)

    review.save()
    return jsonify(review.to_dict()), 200

