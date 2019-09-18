from flask import jsonify


def error_response(status_code, message=None):
    response = {'code': status_code}
    if message:
        response['message'] = message
    return jsonify(response)

# код 400 используется чтобы обозначить «Bad Request».
# код 201 в HTTP означает «Created».

