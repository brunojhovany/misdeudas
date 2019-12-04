from flask import Flask
from flask_restful import Api
from flask_sqlalchemy import SQLAlchemy


import os
app = Flask(__name__)
app.config.from_object(os.environ['APP_SETTINGS'])
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)
api = Api(app)


import controllers.usuariocontroller


api.add_resource(controllers.usuariocontroller.UsuarioLogin, '/login')
api.add_resource(controllers.usuariocontroller.UsuarioLogout, '/logout')
api.add_resource(controllers.usuariocontroller.AllUsers, '/usuario')
api.add_resource(controllers.usuariocontroller.UsuarioRegister, '/registro')
api.add_resource(controllers.usuariocontroller.TestEncryption, '/testencryption')
