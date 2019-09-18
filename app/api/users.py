from app.api import bp
from app.api.auth import token_auth
# from app.api.errors import error_response
from app.api.logging import logging_request
from app.api.tokens import generate_confirmation_token
from app.models import User
from flask import jsonify, request, g
import app.api.errors as apiErr

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
        raise apiErr.NotFoundError('User not found.')
    if g.current_user.get_id != user.get_id:
        raise apiErr.RightsError('Insufficient rights.')
    return jsonify(user.to_dict(include_email=True))


@bp.route('/users', methods=['GET'])
@token_auth.login_required
@logging_request()
def get_users():
    """ Возвращает коллекцию всех пользователей. """
    data = User.to_collection_dict()
    if not data:  # в теории невозможно
        raise apiErr.NotFoundError('Users not found.')
        # return error_response(303, 'Users not found.')
    return jsonify(data)


@bp.route('/users', methods=['POST'])
@logging_request()
def create_user():
    """ Регистрирует новую учетную запись пользователя. """
    data = request.get_json() or {}
    if 'username' not in data or 'email' not in data or 'password' not in data:
        raise apiErr.InsufficientDataError('Must include username, email and password fields.')

    if User.get_or_none(User.username == data['username']):
        raise apiErr.NameUsedError('Please use a different username.')

    if User.get_or_none(User.email == data['email']):
        raise apiErr.EmailUsedError('Please use a different email address.')

    user = User()
    user.from_dict(data, new_user=True)
    user.save()
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
        raise apiErr.NotFoundError('Users not found.')
    if g.current_user.get_id != user.get_id:
        raise apiErr.RightsError('Insufficient rights.')

    data = request.get_json() or {}

    if 'username' in data and data['username'] != user.username and \
            User.get_or_none(User.username == data['username']):
        raise apiErr.NameUsedError('Please use a different username.')
    if 'email' in data and data['email'] != user.email and \
            User.get_or_none(User.email == data['email']):
        raise apiErr.EmailUsedError('Please use a different email address.')

    user.from_dict(data, new_user=False)
    user.save()
    return jsonify(user.to_dict(include_email=True))
