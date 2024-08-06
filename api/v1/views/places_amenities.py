#!/usr/bin/python3
"""
Module contains all default RESTFul API actions for
the Amenity object linked with Place object
"""

from api.v1.views import app_views
from flask import abort, jsonify, request
from models import storage
from models.place import Place
from models.amenity import Amenity


@app_views.route('/places/<place_id>/amenities', strict_slashes=False)
def placeAmenities(place_id):
    """
    Fetches all amenities linked to a Place
    """
    place = storage.get(Place, place_id)

    if not place:
        abort(404)

    amenities = place.amenities

    return jsonify([amenity.to_dict() for amenity in amenities.values()])


@app_views.route('/places/<place_id>/amenities/<amenity_id>',
                 methods=['DELETE', 'POST'], strict_slashes=False)
def deletePlaceAmenity(place_id, amenity_id):
    """
    Deletes an amenity linked to a place
    """
    place = storage.get(Place, place_id)
    amenity = storage.get(Amenity, amenity_id)

    if not place or not amenity:
        abort(404)

    amenities = place.amenities

    if request.method == 'DELETE':
        if 'Amenity.' + amenity_id not in amenities:
            abort(404)

        storage.delete(amenity)
        storage.save()
        return jsonify({}), 200

    if request.method == 'POST':
        statusCode = 200
        if 'Amenity.' + amenity_id not in amenities:
            statusCode = 201
            amenities.append(amenity)
            storage.save()

        return jsonify(amenity.to_dict()), statusCode
