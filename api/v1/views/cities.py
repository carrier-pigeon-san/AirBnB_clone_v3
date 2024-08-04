#!/usr/bin/python3
"""
This module contains a view for City objects that handles all default
RESTful API actions
"""
from flask import jsonify, abort, make_response, request
from api.v1.views import app_views
from models.city import City
from models.state import State
from models import storage


@app_views.route('/cities', strict_slashes = False)
@app_views.route('/states/<state_id>/cities', strict_slashes=False)
def all_cities(state_id):
    """retrieves list of all city objects of a state"""
    state_cities = []
    city_objects = storage.all(City)
    state_objects = storage.all(State)
    state_key = f'State.{state_id}'

    if state_key not in state_objects:
        abort(404)
    for city in city_objects.values():
        if city.state_id == state_id:
            state_cities.append(city.to_dict())
    return jsonify(state_cities), 200


@app_views.route('/cities/<city_id>', strict_slashes=False)
def a_city(city_id):
    """retrieves a city object"""
    city_objects = storage.all(City)
    city_key = f'City.{city_id}'
    if city_key in city_objects:
        return jsonify(city_objects[city_key].to_dict()), 200
    else:
        abort(404)


@app_views.route('/cities/<city_id>', methods=['DELETE'], strict_slashes=False)
def delete_city(city_id):
    """deletes a city object"""
    city_objects = storage.all(City)
    city_key = f'City.{city_id}'
    if city_key in city_objects:
        city_object = city_objects[city_key]
        storage.delete(city_object)
        storage.save()
        return make_response(jsonify({}), 200)
    else:
        abort(404)


@app_views.route('/states/<state_id>/cities', methods=['POST'], strict_slashes=False)
def create_city(state_id):
    """creates a city"""
    state_key = f'State.{state_id}'
    if state_key not in storage.all(State):
        abort(404)
    request_data = request.get_json()
    if request_data is None:
        return make_response("Not a JSON", 400)
    if "name" not in request_data:
        return make_response("Missing name", 400)
    new_city = City(**request_data)
    new_city.state_id = state_id
    new_city.save()
    return jsonify(new_city.to_dict()), 201


@app_views.route('/cities/<city_id>', methods=['PUT'], strict_slashes=False)
def update_city(city_id):
    """updates a city"""
    city_objects = storage.all(City)
    city_key = f'City.{city_id}'
    if city_key not in city_objects:
        abort(404)
    request_data = request.get_json()
    if request_data is None:
        return make_response("Not a JSON", 400)
    city_object = city_objects[city_key]
    for key, value in request_data.items():
        if key not in ("id", "state_id", "created_at", "updated_at"):
            setattr(city_object, key, value)
    city_object.save()
    return jsonify(city_object.to_dict()), 200
