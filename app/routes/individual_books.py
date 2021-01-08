from flask import request, abort, Response, Blueprint, jsonify
from flask_jwt import jwt_required, current_identity
from app.models.models import User, Individual_Book_Posts
from app.models.schema import UserSchema, IndividualBookPostSchema
from app.models import db
import datetime
import math
import os

individual_books = Blueprint('individual_books', __name__)

# Key stored in environment variable using 'export'
google_api_key = os.environ['GOOGLE_API_KEY']

# POST request to add books to user profile
# Accepts a json of all books to be added
# E.g.
# {
#     "books": [
#         {
#             "book_api_id": "alskdfjnalsd",
#             "title": "Red Rising",
#             "cover_img": "https://linkhere.com",
#             "link": "https://imgurlhere.com",
#         }
#     ]
# }
@individual_books.route('/api/new_individual_book/', methods=['POST'])
# @jwt_required()
def add_individual_books():
    books = request.json.get('books')

    if not books:
        abort(400)
    
    for book in books:
        
        #Check if book already exists for current user
        exists = Individual_Book_Posts.query.filter_by(user_id=1).filter_by(book_api_id=book['book_api_id']).first()
        if exists:
            continue

        created = Individual_Book_Posts(book_api_id=book['book_api_id'],
                                        title=book['title'],
                                        cover_img=book['cover_img'],
                                        link=book['link'],
                                        created_time=datetime.datetime.utcnow(),
                                        user_id=1)
        db.session.add(created)
        db.session.commit()
        db.session.refresh(created)
    

    return Response(status=201)

# GET request to get books associated with user
# Returns a json object of all of the books that 
# were added by a user
@individual_books.route('/api/get_user_books/', methods=['GET'])
def get_user_books():
    user_id = request.args.get('user_id')
    user_books = Individual_Book_Posts.query.filter_by(user_id=user_id)
    books_schema = IndividualBookPostSchema(many=True)
    return books_schema.jsonify(user_books)

# POST request to delete book associated with user
# Delete book for certain user
# Requires book_api_id and user identity
@individual_books.route('/api/delete_user_book/', methods=['DELETE'])
@jwt_required()
def delete_user_book():
    book_api_id = request.args.get('book_api_id')
    
    if not book_api_id:
        abort(400)

    book = Individual_Book_Posts.query.filter_by(book_api_id=book_api_id).filter_by(user_id=current_identity.user_id).first()
    if not book:
        return abort(404)

    db.session.delete(book)
    db.session.commit()
    
    return Response(status=200)
