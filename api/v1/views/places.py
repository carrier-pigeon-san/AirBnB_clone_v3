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


@app_views.route('/cities/<city_id>/places', methods=['GET', 'POST'], strict_slashes=False)
def city_places(city_id):
    """
    Gets or adds new place
    """
    city = storage.get(City, city_id)

    if not city:
        abort(404)
    
    places = city.places

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

        if not storage.get(User, req_body['user_id']):
            abort(404)

        place = Place(**req_body)
        storage.new(place)
        city['places'].append(place)
        storage.save()
        return jsonify(place.to_dict()), 201
    
@app_views.route('/places/<place_id>', methods=['GET', 'POST', 'DELETE', 'PUT'], strict_slashes=False)
def places(place_id=None):
    """
    """
    place = storage.get(Place, place_id)

    if not place:
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