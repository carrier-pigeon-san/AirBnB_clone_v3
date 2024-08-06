#!/usr/bin/python3
"""
This module contains a view for User object that handles all default RESTful
API actions
"""

from api.v1.views import app_views
from flask import jsonify, abort, request
from models import storage
from models.user import User


@app_views.route('/users', methods=['GET'], strict_slashes=False)
def list_users():
    """retrieves a list of all user objects using GET method"""
    users = storage.all(User)

    return jsonify([user.to_dict() for user in users.values()])


@app_views.route('/users/<user_id>', methods=['GET'], strict_slashes=False)
def a_user(user_id):
    """retrieves a user object using GET method"""
    user_objects = storage.all(User)
    user_key = "User." + user_id
    if user_key not in user_objects:
        abort(404)
    return jsonify(user_objects[user_key].to_dict())


@app_views.route('/users/<user_id>', methods=['DELETE'], strict_slashes=False)
def delete_user(user_id):
    """deletes a user object using DELETE method"""
    user_objects = storage.all(User)
    user_key = "User." + user_id
    if user_key not in user_objects:
        abort(404)
    user = user_objects[user_key]
    storage.delete(user)
    storage.save()
    return jsonify({}), 200


@app_views.route('/users', methods=['POST'], strict_slashes=False)
def create_user():
    """creates a user using POST method"""
    if not request.is_json:
        abort(400, 'Not a JSON')

    request_data = request.get_json()

    if "email" not in request_data:
        abort(400, "Missing email")
    if "password" not in request_data:
        abort(400, "Missing password")
    new_user = User(**request_data)
    storage.new(new_user)
    storage.save()
    return jsonify(new_user.to_dict()), 201


@app_views.route('/users/<user_id>', methods=['PUT'], strict_slashes=False)
def update_user(user_id):
    """updates a user using PUT method"""
    if not request.is_json:
        abort(400, "Not a JSON")

    user_objects = storage.all(User)
    user_key = "User." + user_id

    if user_key not in user_objects:
        abort(404)

    request_data = request.get_json()
    user = user_objects[user_key]

    for key, value in request_data.items():
        if key not in ("id", "email", "created_at", "updated_at"):
            setattr(user, key, value)

    storage.save()
    return jsonify(user.to_dict()), 200
