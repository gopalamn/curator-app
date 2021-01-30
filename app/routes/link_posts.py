from flask import request, abort, Response, Blueprint, jsonify
from flask_jwt import jwt_required, current_identity
from app.models.models import User, Individual_Book_Posts, Link_Posts
from app.models.schema import UserSchema, IndividualBookPostSchema, LinkPostSchema
from app.models import db
import datetime
import math
import os

link_posts = Blueprint('link_posts', __name__)

# POST request to add link to user profile
# Accepts a json of a link object
# E.g.
# {     
# "link": "alskdfjnalsd",
# "title": "Red Rising",
# "img": "https://linkhere.com",
# "description": "https://imgurlhere.com",
# }
@link_posts.route('/api/new_link_post/', methods=['POST'])
@jwt_required()
def add_link_posts():
    link = request.json.get("link")
    title = request.json.get("title")
    img = request.json.get("img")
    description = request.json.get("description")

    if not link:
        abort(400)
            
    #Check if link already exists for current user current_identity.user_id
    exists = Link_Posts.query.filter_by(user_id=1).filter_by(link=link).first()
    if exists:
        return Response(status=200)

    created = Link_Posts(link=link,
                         title=title,
                         img=img,
                         description=description,
                         created_time=datetime.datetime.utcnow(),
                         user_id=1)
    db.session.add(created)
    db.session.commit()
    db.session.refresh(created)
    

    return Response(status=201)

# GET request to get books associated with user
# Returns a json object of all of the links that 
# were added by a user
@link_posts.route('/api/get_user_links/', methods=['GET'])
def get_user_links():
    user_id = request.args.get('user_id')
    user_links = Link_Posts.query.filter_by(user_id=user_id)
    links_schema = LinkPostSchema(many=True)
    return links_schema.jsonify(user_links)

# POST request to delete link associated with user
# Delete link for certain user
# Requires link_post_id and user identity
@link_posts.route('/api/delete_user_link/', methods=['DELETE'])
@jwt_required()
def delete_user_link():
    link_post_id = request.args.get('link_post_id')
    
    if not link_post_id:
        abort(400)

    link = Link_Posts.query.filter_by(link_post_id=link_post_id).filter_by(user_id=1).first()
    if not link:
        return abort(404)

    db.session.delete(link)
    db.session.commit()
    
    return Response(status=200)
