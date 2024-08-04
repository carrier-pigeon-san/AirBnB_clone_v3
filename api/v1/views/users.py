#!/usr/bin/python3
"""
This module contains a view for User object that handles all default RESTful
API actions
"""

from models import storage
from models.user import User
from flask import jsonify, abort, request
from api.v1.views import app_views


@app_views.route('/users', methods=['GET'], strict_slashes=False)
def list_users():
    """retrieves a list of all user objects"""
    users = []
    user_objects = storage.all(User)
    for user in user_objects.values():
        users.append(user.to_dict())
    return jsonify(users), 200


@app_views.route('/users/<user_id>', methods=['GET'], strict_slashes=False)
def a_user(user_id):
    """retrieves a user object"""
    user_objects = storage.all(User)
    user_key = f"User.{user_id}"
    if user_key not in user_objects:
        abort(404)
    return jsonify(user_objects[user_key].to_dict()), 200


@app_views.route('/users/<user_id>', methods=['DELETE'], strict_slashes=False)
def delete_user(user_id):
    """deletes a user object"""
    user_objects = storage.all(User)
    user_key = f"User.{user_id}"
    if user_key not in user_objects:
        abort(404)
    user = user_objects[user_key]
    storage.delete(user)
    storage.save()
    return jsonify({}), 200


@app_views.route('/users', methods=['POST'], strict_slashes=False)
def create_user():
    """creates a user"""
    request_data = request.get_json()
    if not request_data:
        abort(400, "Not a JSON")
    if "email" not in request_data:
        abort(400, "Missing email")
    if "password" not in request_data:
        abort(400, "Missing password")
    new_user = User(**request_data)
    new_user.save()
    return jsonify(new_user.to_dict()), 201


@app_views.route('/users/<user_id>', methods=['PUT'], strict_slashes=False)
def update_user(user_id):
    """updates a user"""
    user_objects = storage.all(User)
    user_key = f"User.{user_id}"
    if user_key not in user_objects:
        abort(404)
    request_data = request.get_json()
    if not request_data:
        abort(400, "Not a JSON")
    user = user_objects[user_key]
    for key, value in request_data.items():
        if key not in ("id", "email", "created_at", "updated_at"):
            setattr(user, key, value)
    user.save()
    return jsonify(user.to_dict()), 200
