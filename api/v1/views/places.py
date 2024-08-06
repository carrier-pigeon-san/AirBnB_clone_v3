#!/usr/bin/python3
"""
Handles all default RESTFul API actions for the Place object
"""

from api.v1.views import app_views
from flask import request, jsonify, abort
from models import storage
from models.city import City
from models.place import Place
from models.user import User


@app_views.route('/cities/<city_id>/places',
                 methods=['GET', 'POST'],
                 strict_slashes=False)
def city_places(city_id):
    """
    Gets or adds new place
    """
    cities = storage.all(City)
    city_key = "City." + city_id

    if city_key not in cities:
        abort(404)

    places = cities[city_key].places

    if request.method == 'GET':
        return jsonify([place.to_dict() for place in places])

    if request.method == "POST":
        if not request.is_json:
            abort(400, 'Not a JSON')

        req_body = request.get_json()
        req_body['city_id'] = city_id

        if 'name' not in req_body:
            abort(400, 'Missing name')

        if 'user_id' not in req_body:
            abort(400, 'Missing user_id')

        users = storage.all(User)
        user_key = "User." + req_body['user_id']

        if user_key not in users:
            abort(404)

        place = Place(**req_body)
        storage.new(place)
        storage.save()
        return jsonify(place.to_dict()), 201


@app_views.route('/places/<place_id>',
                 methods=['GET', 'DELETE', 'PUT'],
                 strict_slashes=False)
def places(place_id=None):
    """
    Defines GET, DELETE, and PUT actions for
    Place object
    """
    places = storage.all(Place)
    place_key = "Place." + place_id
    place = places[place_key]

    if place_key not in places:
        abort(404)

    if request.method == 'GET':
        return jsonify(place.to_dict()), 200

    if request.method == 'DELETE':
        storage.delete(place)
        storage.save()
        return jsonify({}), 200

    if request.method == 'PUT':
        if not request.is_json:
            abort(400, 'Not a JSON')

        req_body = request.get_json()

        for key, val in req_body.items():
            if key in ['id', 'user_id', 'city_id', 'created_at', 'updated_at']:
                continue
            setattr(place, key, val)

        storage.save()
        return jsonify(place.to_dict()), 200
