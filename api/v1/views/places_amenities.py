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
    places = storage.all(Place)
    key = 'Place.' + place_id

    if key not in places:
        abort(404)

    place = places[key]
    amenities = place.amenities

    return jsonify([amenity.to_dict() for amenity in amenities])


@app_views.route('/places/<place_id>/amenities/<amenity_id>',
                 methods=['DELETE'], strict_slashes=False)
def deletePlaceAmenity(place_id, amenity_id=None):
    """
    Deletes an amenity linked to a place
    """
    if not amenity_id:
        abort(404)

    places = storage.all(Place)
    placeKey = 'Place.' + place_id

    if placeKey not in places:
        abort(404)

    place = places[placeKey]
    amenities = place.amenities
    amenityKey = 'Amenity.' + amenity_id

    if amenityKey not in amenities:
        abort(404)

    amenity = amenities[amenityKey]

    storage.delete(amenity)
    storage.save()
    return jsonify({}), 200


@app_views.route('/places/<place_id>/amenities/<amenity_id>',
                 methods=['DELETE'], strict_slashes=False)
def postPlaceAmenity(place_id, amenity_id=None):
    """
    Adds an amenity object to a place
    """
    if not amenity_id:
        abort(404)
    
    places = storage.all(Place)
    placeKey = 'Place.' + place_id

    if placeKey not in places:
        abort(404)

    amenities = storage.all(Amenity)
    amenityKey = 'Amenity.' + amenity_id

    if amenityKey not in amenities:
        abort(404)

    placeAmenities = places[placeKey].amenities
    amenity = amenities[amenityKey]

    statusCode = 200

    if amenityKey not in placeAmenities:
        statusCode = 201
        placeAmenities.append(amenity)
        storage.save()

    return jsonify(amenity.to_dict()), statusCode
