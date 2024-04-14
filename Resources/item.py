from flask import request
from data import Products
from generateuuid import uuid4
from flask_smorest import Blueprint,abort
from flask.views import MethodView
from marshmallow import Schema,fields
from flask_jwt_extended import jwt_required

class ItemsGetValidation(Schema):
    ProductID=fields.Int(dump_only=True)
    Name=fields.Str(dump_only=True)
    Brand=fields.Str(dump_only=True)
    Category=fields.Str(dump_only=True)
    Price=fields.Float(dump_only=True)
    Quantity=fields.Int(dump_only=True)
class ItemsGetOptional(Schema):
    ProductID=fields.Int(requires=True)
class ItemPostSchema(Schema):
    Name=fields.Str(required=True)
    Brand=fields.Str(required=True)
    Category=fields.Str(required=True)
    Price=fields.Float(required=True)
    Quantity=fields.Int(required=True)

class ItemPutSchemaforbody(Schema):
    Name=fields.Str(requires=True)
    Brand=fields.Str(requires=True)
    Category=fields.Str(requires=True)
    Price=fields.Float(requires=True)
    Quantity=fields.Int(requires=True)
class ItemPutSchemaforID(Schema):
    ProductID=fields.Int(required=True)




blp=Blueprint('Items : Operations on items',__name__)

@blp.route('/item')
class Item(MethodView):
    def __init__(self):
        self.data=Products()
    @jwt_required()
    @blp.response(200,ItemsGetValidation(many=True))
    @blp.arguments(ItemsGetOptional,location="query")
    def get(self,args):
        id=args.get('ProductID')
        print(id)
        if id is None:
            return self.data.get_items()
        else:
            try:
                return self.data.get_item(id)
            except UnboundLocalError:
                abort(404,message="Record doesn't exists")
    @jwt_required()
    @blp.arguments(ItemPostSchema)
    def post(self,body):
        self.data.post_item(body)
        return {'message': 'Item added Successfully.'},201
    @jwt_required()
    @blp.arguments(ItemPutSchemaforbody)
    @blp.response(200,ItemPutSchemaforbody)
    @blp.arguments(ItemPutSchemaforID,location="query")
    def put(self,body,args):
        id=args.get('ProductID')
        if self.data.put_item(id,body):
            return {'message':'Item updated successfully'}
        abort(404,message="Give Id dosen't exists.")
    @jwt_required()
    @blp.arguments(ItemsGetOptional)    
    def delete(self,args):
        id=args.get('ProductID')
        if self.data.delete_item(id):
            return {'message':'Item deleted successfully.'}
        abort(404,message="Give Id dosen't exists.")
        

