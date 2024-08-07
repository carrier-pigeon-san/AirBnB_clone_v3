#!/usr/bin/python3
"""This module contains a view for the relationship between places and
amenities and handles all default RESTful API actions"""
from api.v1.views import app_views
from flask import abort, jsonify, request
from models.amenity import Amenity
from models.place import Place
from models import storage
from models import storage_t
from os import getenv


@app_views.route('/places/<place_id>/amenities', methods=['GET'],
                 strict_slashes=False)
def list_place_amenities(place_id):
    """Retrieves the list of all Amenity objects of a Place"""
    place = storage.get(Place, place_id)
    if not place:
        abort(404)
    if storage_t != 'db':
        amenities = []
        for id in place.amenity_ids:
            amenities.append(storage.get(Amenity, id).to_dict())
        return jsonify(amenities), 200
    amenities = [amenity.to_dict() for amenity in place.amenities]
    return jsonify(amenities), 200


@app_views.route('/places/<place_id>/amenities/<amenity_id>',
                 methods=['DELETE'], strict_slashes=False)
def delete_amenity(place_id, amenity_id):
    """Deletes an Amenity object to a Place"""
    place = storage.get(Place, place_id)
    amenity = storage.get(Amenity, amenity_id)
    if not place or not amenity or amenity not in place.amenities:
        abort(404)

    if storage_t != 'db':
        place.amenity_ids.remove(amenity_id)
        storage.save()
        return jsonify({}), 200
    place.amenities.remove(amenity)
    storage.save
    return jsonify({}), 200


@app_views.route('/places/<place_id>/amenities/<amenity_id>',
                 methods=['POST'], strict_slashes=False)
def create_amenity(place_id, amenity_id):
    """Links an Amenity object to a Place"""
    place = storage.get(Place, place_id)
    amenity = storage.get(Amenity, amenity_id)
    if not place or not amenity:
        abort(404)

    if storage_t != 'db':
        if amenity_id in place.amenity_ids:
            return jsonify(amenity.to_dict()), 200
        place.amenity_ids.append(amenity_id)
        storage.save()
        return jsonify(amenity.to_dict()), 201
    if amenity in place.amenities:
        return jsonify(amenity.to_dict()), 200
    place.amenities.append(amenity)
    storage.save()
    return jsonify(amenity.to_dict()), 201
