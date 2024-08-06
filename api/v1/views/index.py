#!/usr/bin/python3
"""
Creates flask app using the app_views blueprint
Creates '/status' route that returns JSON with status 'OK'
"""

from api.v1.views import app_views
from flask import Flask, jsonify
from models import storage
from models.amenity import Amenity
from models.city import City
from models.place import Place
from models.review import Review
from models.state import State
from models.user import User


@app_views.route('/status', strict_slashes=False)
def getStatus():
    """
    Returns json of status
    """
    return jsonify({"status": "OK"})


@app_views.route('/stats')
def count():
    """retrieves number of each object by type"""
    classes = {"amenities": Amenity, "cities": City, "places": Place,
               "reviews": Review, "states": State, "users": User}
    count = {}
    for k, v in zip(classes.keys(), classes.values()):
        count_val = storage.count(v)
        count[k] = count_val
    return jsonify(count)
