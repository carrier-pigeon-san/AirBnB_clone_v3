#!/usr/bin/python3
"""
Creates flask app using the app_views blueprint
Creates '/status' route that returns JSON with status 'OK'
"""

from api.v1.views import app_views
from flask import Flask, jsonify


@app_views.route('/status')
def status():
    """
    Returns json of status
    """
    return jsonify({"status": "OK"})
