#!/usr/bin/python3
"""
Handles all default RESTFul API actions for the Place object
"""

from api.v1.views import app_views
from flask import request, jsonify, abort
from models import storage
from models.city import City
from models.place import Place


@app_views.route('/cities/<city_id>/places', methods=['GET', 'POST'], strict_slashes=False)
@app_views.route('/cities/<city_id>/places/<place_id>',
                 methods=['GET', 'DELETE', 'PUT'],
                 strict_slashes=False)
def places(city_id, place_id=None):
    city = storage.get(City, city_id)

    if not city:
        abort(404)
    
    places = city.places
    place = storage.get(Place, place_id)

    if request.method == 'GET':
        if not place_id:
            return jsonify([place.to_dict() for place in places])

        if not place:
            abort(404)

        return jsonify(place.to_dict())

    if request.method == "DELETE":
        if not place:
            abort(404)

        storage.delete(place)
        storage.save()
        return jsonify({}), 200

    if request.method == "POST":
        if not request.is_json:
            abort(400, 'Not a JSON')

        req_body = request.get_json()

        if 'name' not in req_body:
            abort(400, 'Missing name')

        place = Place(**req_body)
        storage.new(place)
        storage.save()
        return jsonify(place.to_dict()), 201

    if request.method == "PUT":
        if not place:
            abort(404)

        if not request.is_json:
            abort(400, 'Not a JSON')

        req_body = request.get_json()

        for key, val in req_body.items():
            if key in ["id", "created_at", "updated_at"]:
                continue
            setattr(place, key, val)

        storage.save()
        return jsonify(place.to_dict()), 200
