#!/usr/bin/python3
"""
Handles all default RESTFul API actions for the State object
"""

from api.v1.views import app_views
from flask import request, jsonify, abort
from models import storage
from models.state import State


@app_views.route('/states', methods=['GET', 'POST'], strict_slashes=False)
@app_views.route('/states/<state_id>',
                 methods=['GET', 'DELETE', 'PUT'],
                 strict_slashes=False)
def states(state_id=None):
    states = storage.all('State')
    key = 'State.' + state_id if state_id else None

    if request.method == 'GET':
        if not key:
            return jsonify([state.to_dict() for state in states.values()])

        if key not in states.keys():
            abort(404)

        return jsonify(states[key].to_dict())

    if request.method == "DELETE":
        if key not in states.keys():
            abort(404)

        storage.delete(states[key])
        storage.save()
        return jsonify({}), 200

    if request.method == "POST":
        if not request.is_json:
            abort(400, 'Not a JSON')

        req_body = request.get_json()

        if 'name' not in req_body:
            abort(400, 'Missing name')

        state = State(**req_body)
        storage.new(state)
        storage.save()
        return jsonify(state.to_dict()), 201

    if request.method == "PUT":
        if key not in states.keys():
            abort(404)

        if not request.is_json:
            abort(400, 'Not a JSON')

        req_body = request.get_json()

        state = states[key]

        for key, val in req_body.items():
            if key in ["id", "created_at", "updated_at"]:
                continue
            setattr(state, key, val)

        storage.save()
        return jsonify(state.to_dict()), 200
