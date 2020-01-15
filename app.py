from flask import Flask
from flask_restful import Api
from flask_sqlalchemy import SQLAlchemy
from flask_jwt_extended import JWTManager
import os
from flask_migrate import Migrate

app = Flask(__name__)
app.config.from_object(os.environ['APP_SETTINGS'])
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['JWT_SECRET_KEY'] = os.environ['JWTSECRET']
app.config['PROPAGATE_EXCEPTIONS'] = True
app.config['JWT_BLACKLIST_ENABLED'] = True
app.config['JWT_BLACKLIST_TOKEN_CHECKS'] = ['access', 'refresh']
db = SQLAlchemy(app)
migrate = Migrate(app, db)
api = Api(app)
jwt = JWTManager(app)


import controllers.usuariocontroller
import controllers.admonappcontroller
import controllers.deudacontroller
from models.entities import Rol_Por_Usuario, RevokedTokenModel


@jwt.token_in_blacklist_loader
def check_if_token_in_blacklist(decrypted_token):
    jti = decrypted_token['jti']
    return RevokedTokenModel.is_jti_blacklisted(jti)


@jwt.user_claims_loader
def add_claims_to_access_token(user):
    return {'roles': Rol_Por_Usuario.get_roles(user.roles)}


@jwt.user_identity_loader
def user_identity_lookup(user):
    return user.nombre_usuario

def setup_app(app):
    # Create tables if they do not exist already
    @app.before_first_request
    def create_tables():
        db.create_all()


setup_app(app)


api.add_resource(controllers.usuariocontroller.AllUsers, '/usuario')
api.add_resource(controllers.usuariocontroller.UsuarioRegister, '/registro')
api.add_resource(controllers.usuariocontroller.UsuarioLogin, '/auth/login')
api.add_resource(controllers.usuariocontroller.TokenRefresh, '/auth/refresh')
api.add_resource(controllers.usuariocontroller.UsuarioLogout, '/auth/logout/access')
api.add_resource(controllers.usuariocontroller.UsuarioLogoutRefresh, '/auth/logout/refresh')
api.add_resource(controllers.usuariocontroller.TestSecurity, '/testsecurity')

api.add_resource(controllers.admonappcontroller.Estatus, '/admon/estatus')
api.add_resource(controllers.admonappcontroller.Entidad_Bancaria, '/admon/Entidad_Bancaria')


api.add_resource(controllers.deudacontroller.deuda_del_mes, '/control/deuda-del-mes')
