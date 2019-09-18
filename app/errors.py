from app import app
from flask import make_response, jsonify
# from app.api.errors import error_response as api_error_response
import app.api.errors as apiErr


@app.errorhandler(Exception)
def api_error(error):
    if isinstance(error, apiErr.ApiError):
        return error.make_response()

    return make_response(jsonify({
        'message': 'Internal error',
        'code': -1
    }), 500)
