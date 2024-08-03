#!/usr/bin/python3
"""
Creates a flask app
"""

from api.v1.views import app_views
from flask import Flask, jsonify
from models import storage
from os import getenv

app = Flask(__name__)
app.register_blueprint(app_views)


@app.teardown_appcontext
def tear_down(arg=None):
    storage.close()


@app.errorhandler(404)
def not_found():
    """
    Returns json representation of 404 error
    """
    return jsonify({"error": "Not found"})


if __name__ == "__main__":
    HOST = getenv("HBNB_API_HOST") or '0.0.0.0'
    PORT = int(getenv("HBNB_API_PORT")) or 5000
    app.run(host=HOST, port=PORT, threaded=True)
