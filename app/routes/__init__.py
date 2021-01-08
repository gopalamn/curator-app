from .test import test
from .users import users
from app.models.models import User
from app.models.schema import UserSchema
from flask_jwt import JWT
from flask import jsonify
import bcrypt

def init_app(app):
    jwt.init_app(app)
    app.register_blueprint(test)
    app.register_blueprint(users)

def authenticate(email, password):
    user = User.query.filter_by(email=email).first()
    if user and bcrypt.checkpw(password.encode('utf8'), user.password_hash.encode('utf8')):
        user.id = user.user_id
        return user

def identity_fn(payload):
    user_id = payload['identity']
    return User.query.get(user_id)

jwt = JWT(authentication_handler=authenticate, identity_handler=identity_fn)

@jwt.auth_response_handler
def customized_response_handler(access_token, identity):
    return jsonify({
        'access_token': access_token.decode('utf8'),
        'user_id': identity.user_id,
        'username': identity.username,
        'email': identity.email,
        'profile_pic': identity.profile_pic
    })