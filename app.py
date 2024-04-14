from flask import Flask
from Resources.item import blp as ItemBluePrint
from Resources.user import blp as UserBluePrint
from flask_smorest import Api
from flask_jwt_extended import JWTManager
from BlockedTokenList import BlockedTokenList

app=Flask(__name__)

app.config["PROPAGATE_EXCEPTIONS"]=True
app.config["API_TITLE"]="MY First API"
app.config["API_VERSION"]="v1"
app.config["OPENAPI_VERSION"]="3.0.3"
app.config["OPENAPI_URL_PREFIX"]="/"
app.config["OPENAPI_SWAGGER_UI_PATH"]="swagger-ui"
app.config["OPENAPI_SWAGGER_UI_URL"]="https://cdn.jsdelivr.net/npm/swagger-ui-dist/"
app.config["JWT_SECRET_KEY"]="128049257485979450042506981494033807800"

api=Api(app)
jwt=JWTManager(app)
@jwt.token_in_blocklist_loader
def Blocked_List(headerOFjwt,payloadOfjwt):
    return payloadOfjwt["jti"] in BlockedTokenList

@jwt.revoked_token_loader
def Response(headerOFjwt,payloadOfjwt):
    return(
        {
            "message":"Access denied! Yo need to be authorized to perform this action"
        },
        401
    )
api.register_blueprint(ItemBluePrint)
api.register_blueprint(UserBluePrint)




