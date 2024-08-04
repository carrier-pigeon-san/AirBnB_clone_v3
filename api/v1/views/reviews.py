#!/usr/bin/python3
"""
This module contains a new view for Review object that handles all default
RESTful API actions.
"""
from flask import abort, jsonify, request
from api.v1.views import app_views
from models.review import Review
from models.place import Place
from models.user import User
from models import storage


@app_views.route('/places/<place_id>/reviews', methods=['GET'],
                 strict_slashes=False)
def all_reviews(place_id):
    """retrieves the list of all Review objects of a Place"""
    place_reviews = []
    reviews = storage.all(Review)
    places = storage.all(Place)
    place_key = f"Place.{place_id}"
    if place_key not in places:
        abort(404)
    for review in reviews.values():
        if review.place_id == place_id:
            place_reviews.append(review.to_dict())
    return jsonify(place_reviews), 200


@app_views.route('/reviews', strict_slashes=False)
@app_views.route('/reviews/<review_id', methods=['GET'], strict_slashes=False)
def a_review(review_id):
    """retrieves a review object"""
    reviews = storage.all(Review)
    review_key = f"Review.{review_id}"
    if review_key not in reviews:
        abort(404)
    review = reviews[review_key]
    return jsonify(review.to_dict()), 200


@app_views.route('/reviews/<review_id', methods=['DELETE'], strict_slashes=False)
def delete_reviews(review_id):
    """deletes a review object"""
    reviews = storage.all(Review)
    review_key = f"Review.{review_id}"
    if review_key not in reviews:
        abort(404)
    storage.delete(reviews[review_key])
    storage.save
    return jsonify({}), 200


@app_views.route('/places/<place_id>/reviews', methods=['POST'],
                 strict_slashes=False)
def create_review(place_id):
    """creates a review"""
    places = storage.all(Place)
    users = storage.all(User)
    place_key = f"Place.{place_id}"
    if place_key not in places:
        abort(404)
    request_data = request.get_json()
    if request_data is None:
        abort(400, "Not a JSON")
    if "user_id" not in request_data:
        abort(400, "Missing user_id")
    if "text" not in request_data:
        abort(404, "Missing text")
    user_key = f"User.{request_data.get('user_id')}"
    if user_key not in users:
        abort(404)
    new_review = Review(**request_data)
    new_review.place_id = place_id
    new_review.save()
    return jsonify(new_review.to_dict()), 201


@app_views.route('/reviews/<review_id>', methods=['PUT'], strict_slashes=False)
def update_review(review_id):
    """updates a review object"""
    reviews = storage.all(Review)
    review_key = f"Review.{review_id}"
    if review_key not in reviews:
        abort(404)
    review = reviews[review_key]
    request_data = request.get_json()
    if request_data is None:
        abort(400, "Not a JSON")
    for key, value in request_data.items():
        if key not in ("id", "user_id", "place_id", "created_at",
                       "updated_at"):
            setattr(review, key, value)
    review.save()
    return jsonify(review.to_dict()), 200
