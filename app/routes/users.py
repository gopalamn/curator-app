from flask import request, jsonify, abort, Response, Blueprint
from flask_jwt import jwt_required, current_identity
from app.models.models import User, Individual_Book_Posts
from app.models.schema import UserSchema, IndividualBookPostSchema
from app.models import db
import bcrypt
import boto3
from random import random
import time

users = Blueprint('users', __name__)

try:
    s3 = boto3.client('s3')
except Exception as e:
    print("Exception ", e)

# Checks if there exists a username already
# Returns true if it already exists, false if
# it doesn't exist
def username_exists(username):
    # Don't allow empty usernames
    if not username:
        return True
    
    user_with_username = User.query.filter_by(username=username).first()
    if user_with_username:
        return True
    
    return False

# Checks if there exists an email registered already
# Returns true if it already exists, false if
# it doesn't exist
def email_exists(email):
    # Don't allow empty emails
    if not email:
        return True
    
    user_with_email = User.query.filter_by(email=email).first()
    if user_with_email:
        return True
    
    return False



# Check if an email is already associated with a user
# Returns true if there's an existing user with the email
# and false otherwise
@users.route('/api/check_email/', methods=['GET'])
def check_email():
    email = request.args.get('email')

    exists = email_exists(email)
    
    if exists:
        return jsonify({'exists': True})
    else:
        return jsonify({'exists': False})

# Returns json of user object
@users.route('/api/get_user/', methods=['GET'])
def get_user():
    user_id = request.args.get('user_id')
    if not user_id:
        abort(400)
    user = User.query.get(user_id)
    user_schema = UserSchema()
    return user_schema.jsonify(user)

# Adds user to database, used for signup
@users.route('/api/add_user/', methods=['POST'])
def add_user():
    email = request.json.get('email')
    username = request.json.get('username')
    password = request.json.get('password')
    firstname = request.json.get('firstname')
    lastname = request.json.get('lastname')

    if not email or not username or not password or not firstname or not lastname:
        abort(400)

    # Make sure the username is unique
    user_with_username = User.query.filter_by(username=username).first()
    if user_with_username:
        abort(404)
    
    # Store secure password
    hashed_pwd = bcrypt.hashpw(password.encode('utf8'), bcrypt.gensalt())

    new_user = User(email=email,
                    username=username,
                    password_hash=hashed_pwd,
                    firstname=firstname,
                    lastname=lastname)
    
    db.session.add(new_user)
    db.session.commit()
    db.session.refresh(new_user)

    return Response(status=201)