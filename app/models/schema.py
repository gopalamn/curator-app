from . import ma
from .models import *
from marshmallow import pre_dump

class UserSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = User

class IndividualBookPostSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Individual_Book_Posts
        # Include foreign keys
        include_fk = True
    
    user = ma.Nested(UserSchema)

class LinkPostSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Link_Posts
        #Include foreign keys
        include_fk = True

    user = ma.Nested(UserSchema)