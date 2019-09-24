from flask import jsonify
from app.api import bp
from app.models import User
from app.api.tokens import confirm_token
from app.api.logging import logging_request
import app.api.errors as apiErr


@bp.route('/confirm/<token>')
@logging_request(logging_rr=False)
def confirm(token):
    email = confirm_token(token)
    if not email:
        raise apiErr.InvalidLincError()
    user = User.get_or_none(User.email == email)
    if not user:
        raise apiErr.InvalidLincError()
    if user.confirmed:
        raise apiErr.AlreadyConfirmedError()

    user.confirmed = True
    user.save()
    return jsonify({'message': 'Email confirmed.'})
