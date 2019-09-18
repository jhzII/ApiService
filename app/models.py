import os
import base64
from app import db
import peewee as pw
from datetime import datetime, timedelta
from werkzeug.security import generate_password_hash, check_password_hash


class User(pw.Model):
    class Meta:
        database = db

    username = pw.CharField(64)  # , null=False
    email = pw.CharField(128)
    birthday = pw.DateField(formats='%Y-%m-%d', null=True)
    password_hash = pw.CharField(128)
    confirmed = pw.BooleanField(default=False)
    token = pw.CharField(32, index=True, unique=True, null=True)
    token_expiration = pw.DateField(formats='%Y-%m-%d %H:%M:%S', null=True)

    def get_confirmed(self):
        return self.confirmed

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    def to_dict(self, include_email=False):
        data = {
            'id': self.id,
            'birthday': self.birthday,
            'username': self.username,
            'confirmed': self.confirmed
        }
        if include_email:
            data['email'] = self.email
        return data

    def from_dict(self, data, new_user=False):
        for field in ['username', 'birthday', 'email']:
            if field in data:
                setattr(self, field, data[field])
        if new_user and 'password' in data:  # МБ лишнее
            self.set_password(data['password'])

    def get_token(self, expires_in=3600):
        now = datetime.utcnow()
        if self.token_expiration is not None:
            time_token_expiration = datetime.strptime(self.token_expiration, '%Y-%m-%d %H:%M:%S')
            if self.token and time_token_expiration > now + timedelta(seconds=60):
                return self.token
        self.token = base64.b64encode(os.urandom(24)).decode('utf-8')
        self.token_expiration = (now + timedelta(seconds=expires_in)).strftime('%Y-%m-%d %H:%M:%S')
        self.save()
        return self.token

    def revoke_token(self):
        self.token_expiration = (datetime.utcnow() - timedelta(seconds=1)).strftime('%Y-%m-%d %H:%M:%S')
        self.save()

    @staticmethod
    def check_token(token):
        user = User.get_or_none(User.token == token)
        if user is None:
            return None
        if user.token_expiration is not None:
            time_token_expiration = datetime.strptime(user.token_expiration, '%Y-%m-%d %H:%M:%S')
            if time_token_expiration < datetime.utcnow():
                return None
        return user

    @staticmethod
    def to_collection_dict():
        data = {
            'items': [item.to_dict() for item in User.select()]
        }
        return data

    def __repr__(self):
        return f'<User {self.username}>'
