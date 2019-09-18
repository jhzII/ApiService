from app import app
from app.models import User
from app.api.tokens import confirm_token
from flask import jsonify, render_template, request


@app.route('/confirm/<token>', methods=['GET', 'POST'])
def confirm(token):
    email = confirm_token(token)
    if not email:
        return jsonify({'message': 'Invalid link.', 'code': 102})
    user = User.get_or_none(User.email == email)
    if not user:
        return jsonify({'message': 'Invalid link.', 'code': 102})
    if user.confirmed:
        return jsonify({'message': 'Email has already been confirmed.',
                        'code': 101})
    user.confirmed = True
    user.save()
    return jsonify({'message': 'Email confirmed'})  # , 'code': 200
    # return '', 204
    # код состояния 204 используется для успешных запросов без тела ответа.


@app.route('/hello')
def test():
    return render_template('hello.html', name='User')
