#!/usr/bin/python3
"""
Handles all default RESTFul API actions for the State object
"""

from api.v1.views import app_views
from flask import request, jsonify, abort
from models import storage


@app_views.route('/states', methods=['GET', 'POST'], strict_slashes=False)
@app_views.route('/states/<state_id>',
                 methods=['GET', 'DELETE', 'PUT'],
                 strict_slashes=False)
def get_states(state_id=None):
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
    
    #return jsonify([state.to_dict() for state in states.values()])

