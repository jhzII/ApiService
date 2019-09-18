from app import app
from app.api.errors import error_response as api_error_response


@app.errorhandler(404)
def not_found_error(error):
    return api_error_response(404)


@app.errorhandler(405)
def internal_error(error):
    return api_error_response(405)


@app.errorhandler(500)
def internal_error(error):
    return api_error_response(500)


# from flask import make_response
#
# @app.errorhandler(404)
# def not_found(error):
#     return make_response(jsonify({'error': 'Not found'}), 404)
