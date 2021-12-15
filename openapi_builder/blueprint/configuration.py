from flask import current_app, jsonify

from ..constants import EXTENSION_NAME
from .blueprint import openapi_documentation


@openapi_documentation.route("/configuration", methods=["GET"])
def configuration():
    """Get Open API configuration."""
    return jsonify(current_app.extensions[EXTENSION_NAME].get_configuration())
