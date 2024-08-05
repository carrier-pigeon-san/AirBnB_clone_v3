#!/usr/bin/python3
"""
Handles all default RESTFul API actions for the Amenity object
"""

from api.v1.views import app_views
from flask import request, jsonify, abort
from models import storage
from models.amenity import Amenity


@app_views.route('/amenities', methods=['GET', 'POST'], strict_slashes=False)
@app_views.route('/amenities/<amenity_id>',
                 methods=['GET', 'DELETE', 'PUT'],
                 strict_slashes=False)
def amenities(amenity_id=None):
<<<<<<< HEAD
    """RESTful api actions for Amenity object"""
=======
    """Handles default RESTful actions of Amenity object"""
>>>>>>> master
    amenities = storage.all(Amenity)
    key = 'Amenity.' + amenity_id if amenity_id else None

    if request.method == 'GET':
        if not key:
            return jsonify(
                [amenity.to_dict() for amenity in amenities.values()]
                )

        if key not in amenities.keys():
            abort(404)

        return jsonify(amenities[key].to_dict())

    if request.method == "DELETE":
        if key not in amenities.keys():
            abort(404)

        storage.delete(amenities[key])
        storage.save()
        return jsonify({}), 200

    if request.method == "POST":
        if not request.is_json:
            abort(400, 'Not a JSON')

        req_body = request.get_json()

        if 'name' not in req_body:
            abort(400, 'Missing name')

        amenity = Amenity(**req_body)
        storage.new(amenity)
        storage.save()
        return jsonify(amenity.to_dict()), 201

    if request.method == "PUT":
        if key not in amenities.keys():
            abort(404)

        if not request.is_json:
            abort(400, 'Not a JSON')

        req_body = request.get_json()

        amenity = amenities[key]

        for key, val in req_body.items():
            if key in ["id", "created_at", "updated_at"]:
                continue
            setattr(amenity, key, val)

        storage.save()
        return jsonify(amenity.to_dict()), 200
