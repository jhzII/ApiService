from app.api import bp
from app.api.auth import token_auth
from app.api.errors import error_response
from app.api.logging import logging_request
from app.api.tokens import generate_confirmation_token
from app.models import User
from flask import jsonify, request, g

# @bp.before_request
# def before_request():
#     # print('test - before_request')
#     app.logger.setLevel(logging.INFO)
#     app.logger.info('before info')


# @bp.after_request
# def after_request(response):
#     # print('test - after_request')
#     app.logger.setLevel(logging.INFO)
#     app.logger.info('after info')
#     return response


# @bp.teardown_request
# def teardown_request(response):
#     # print('del 0')
#     return response


@bp.route('/users/<int:id>', methods=['GET'])
@token_auth.login_required
@logging_request(logging_rr=False)
def get_user(id):
    """ Возвращает пользователя. """
    user = User.get_or_none(User.id == id)
    if not user:
        return error_response(301, 'User not found.')   #TODO
    if g.current_user.get_id != user.get_id:
        return error_response(302, 'Insufficient rights.')  #TODO
    return jsonify(user.to_dict(include_email=True))


@bp.route('/users', methods=['GET'])
@token_auth.login_required
@logging_request()
def get_users():
    """ Возвращает коллекцию всех пользователей. """
    data = User.to_collection_dict()
    if not data:  # в теории невозможно
        return error_response(303, 'Users not found.')  #TODO
    return jsonify(data)


@bp.route('/users', methods=['POST'])
@logging_request()
def create_user():
    """ Регистрирует новую учетную запись пользователя. """
    data = request.get_json() or {}
    if 'username' not in data or 'email' not in data or 'password' not in data:
        return error_response(
            304, 'Must include username, email and password fields.')   #TODO

    if User.get_or_none(User.username == data['username']):
        return error_response(305, 'Please use a different username.')  #TODO

    if User.get_or_none(User.email == data['email']):
        return error_response(306, 'Please use a different email address.') #TODO

    user = User()
    user.from_dict(data, new_user=True)
    user.save()
    # МОМЕНТ НИЖЕ НУЖНО УТОЧНИТЬ ----------------------------------------------
    # response = jsonify(user.to_dict(include_email=True))
    # response.status_code = 201  # ТУТ МБ ИЗМЕНИТЬ
    # response.headers['Location'] = url_for('api.get_user', id=user.id)
    token = generate_confirmation_token(user)
    response = jsonify({
        'message': f'Link to confirm email: <domain>/confirm/{token}'})
    return response


@bp.route('/users/<int:id>', methods=['PUT'])
@token_auth.login_required
@logging_request()
def update_user(id):
    """ Изменяет пользователя. """
    user = User.get_or_none(User.id == id)

    if not user:
        return error_response(301, 'User not found.')   #TODO
    if g.current_user.get_id != user.get_id:
        return error_response(302, 'Insufficient rights.')  #TODO

    data = request.get_json() or {}

    if 'username' in data and data['username'] != user.username and \
            User.get_or_none(User.username == data['username']):
        return error_response(305, 'Please use a different username.')  #TODO
    if 'email' in data and data['email'] != user.email and \
            User.get_or_none(User.email == data['email']):
        return error_response(306, 'Please use a different email address.') #TODO

    user.from_dict(data, new_user=False)
    user.save()
    return jsonify(user.to_dict(include_email=True))
