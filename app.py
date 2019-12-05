from flask import Flask
from flask_restful import Api
from flask_sqlalchemy import SQLAlchemy
from flask_jwt_extended import JWTManager
import os

app = Flask(__name__)
app.config.from_object(os.environ['APP_SETTINGS'])
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['JWT_SECRET_KEY'] = os.environ['JWTSECRET']
app.config['PROPAGATE_EXCEPTIONS'] = True
app.config['JWT_BLACKLIST_ENABLED'] = True
app.config['JWT_BLACKLIST_TOKEN_CHECKS'] = ['access', 'refresh']
db = SQLAlchemy(app)
api = Api(app)
jwt = JWTManager(app)


import controllers.usuariocontroller
from models import jwtblacklist


@jwt.token_in_blacklist_loader
def check_if_token_in_blacklist(decrypted_token):
    jti = decrypted_token['jti']
    return jwtblacklist.RevokedTokenModel.is_jti_blacklisted(jti)


api.add_resource(controllers.usuariocontroller.UsuarioLogin, '/login')
api.add_resource(controllers.usuariocontroller.UsuarioLogout, '/logout')
api.add_resource(controllers.usuariocontroller.TokenRefresh, '/refresh_token')
api.add_resource(controllers.usuariocontroller.AllUsers, '/usuario')
api.add_resource(controllers.usuariocontroller.UsuarioRegister, '/registro')
api.add_resource(controllers.usuariocontroller.TestSecurity, '/testsecurity')
