#!/usr/bin/python3


from flask import Flask
from models import storage
from api.v1.views import app_views
from os import getenv

host = getenv("HBNB_API_HOST") or '0.0.0.0'
port = getenv("HBNB_API_PORT") or '5000'

app = Flask(__name__)
app.register_blueprint(app_views)

@app.teardown_appcontext
def tear_down(arg=None):
    storage.close()

if __name__ == "__main__":
    app.run(host=host, port=port, threaded=True)
