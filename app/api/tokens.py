from app import app
from flask import jsonify, g
from app.api import bp
from app.api.auth import basic_auth, token_auth
from itsdangerous import URLSafeSerializer, BadSignature


def generate_confirmation_token(user):
    serializer = URLSafeSerializer(app.config['SECRET_KEY'])
    return serializer.dumps(user.email, salt=app.config['SECURITY_PASSWORD_SALT'])


def confirm_token(token):
    serializer = URLSafeSerializer(app.config['SECRET_KEY'])
    try:
        email = serializer.loads(
            token,
            salt=app.config['SECURITY_PASSWORD_SALT']
        )
    except BadSignature:
        return False
    return email


@bp.route('/tokens', methods=['POST'])
@basic_auth.login_required
def get_token():
    if not g.current_user.get_confirmed():
        token = generate_confirmation_token(g.current_user)
        return jsonify(
            {'message': 'Email not confirmed. Link to confirm email: ' +
                        f'<domen>/confirm/{token}', 'code': 201})
    token = g.current_user.get_token()
    return jsonify({'token': token})


@bp.route('/tokens', methods=['DELETE'])
@token_auth.login_required
def revoke_token():
    g.current_user.revoke_token()
    return '', 204
    # код состояния 204 используется для успешных запросов без тела ответа.
