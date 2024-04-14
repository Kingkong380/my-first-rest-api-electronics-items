from flask_smorest import Blueprint,abort
from flask.views import MethodView
from Userdata import DataOfUser
from marshmallow import Schema,fields
import hashlib 
from flask_jwt_extended import create_access_token,jwt_required,get_jwt
from BlockedTokenList import BlockedTokenList

class UserSchema(Schema):
    id=fields.Int(dump_only=True)
    username=fields.Str(required=True)
    password=fields.Str(required=True,load_only=True)
class UserID(Schema):
    id=fields.Int(required=True)


blp=Blueprint("Users",__name__)

@blp.route('/login')
class UserLogin(MethodView):
    def __init__(self):
        self.userdata=DataOfUser()
    @blp.arguments(UserSchema)
    def post(self,args):
        id=args.get('id')
        username=args.get('username')
        password=hashlib.sha256(args.get('password').encode('utf-8')).hexdigest()
        verified=self.userdata.Verify_user(username,password)
        if verified:
            return {"access_token":create_access_token(identity=verified)}
        abort(400,message="Invalid username or password")

@blp.route('/logout')
class UserLogOut(MethodView):
    @jwt_required()
    def post(self):
        jti=get_jwt()['jti']
        BlockedTokenList.add(jti)
        return {'message':'Successfully logged out'}
        
@blp.route('/user')
class User(MethodView):
    def __init__(self):
        self.userdata=DataOfUser()
    def get(self):
        return self.userdata.get_user()
    @blp.arguments(UserSchema)
    def post(self,args):
        username=args.get('username')
        password=hashlib.sha256(args.get('password').encode('utf-8')).hexdigest()
        #check if user already exists
        if self.userdata.create_user(username,password):
            return {'Message':'User added successfully.'}
        return {'Message':'Failed to add user because user already exists or name has been taken.'}
    @blp.arguments(UserID,location="query")
    def delete(self,args):
        id=args.get('id')
        if self.userdata.delete_user(id):
            return {'message':'User deleted successfully.'}, 200
        abort(403,message="Cannot find entered ID.")
