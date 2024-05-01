#!/usr/bin/python3

from flask import Flask, jsonify
from flask_cors import CORS
from os import getenv
from api.v1.views import app_views
from models import storage


app = Flask(__name__)
app.register_blueprint(app_views)
CORS(app, resources={r"/*": {"origins": "0.0.0.0"}})

@app.teardown_appcontext
def teardown(exception):
    """
    fuction to close storage session
    """
    storage.close()

@app.errorhandler(404)
def not_found(error):

    """handling for 404 errors that returns 
    a JSON-formatted 404 status code response.
    """
    
    return jsonify({"error": "Not found"}), 404


if __name__ == "__main__":
    app.run(
        host=getenv("HBNB_API_HOST", default="0.0.0.0"),
        port=getenv("HBNB_API_PORT", default="5000"),
        threaded=True,
        debug=True
    )
