#!/usr/bin/python3
"""flask app"""
from os import getenv
from flask import Flask, jsonify
from flask_cors import CORS
from api.v1.views import app_views
from models import storage


app = Flask(__name__)
app.url_map.strict_slashes = False
app.register_blueprint(app_views)
CORS(app, resources={r"/*": {"origins": "*"}})


@app.errorhandler(404)
def not_found404(error):
    """ 404 respose handler"""
    return jsonify({"error": "Not found"}), 404


@app.teardown_appcontext
def storage_close(exception):
    """storage section close handler."""
    storage.close()


if __name__ == "__main__":
    app.run(
        host=getenv("HBNB_API_HOST", default="0.0.0.0"),
        port=getenv("HBNB_API_PORT", default="5000"),
        threaded=True,
        debug=True
    )
