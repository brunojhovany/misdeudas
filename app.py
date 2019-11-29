from flask import Flask, jsonify
from flask_restful import Resource, Api
from flask_sqlalchemy import SQLAlchemy

import os
app = Flask(__name__)
app.config.from_object(os.environ['APP_SETTINGS'])
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)
from models import usuario

api = Api(app)


class UsuarioController(Resource):
    def get(self):
        usuarios = usuario.Usuario.query.all()
        return jsonify([e.serialize() for e in usuarios])


api.add_resource(UsuarioController, '/usuario')
# @app.route('/')
# def hello_world():
#     usuarios = usuario.Usuario.query.all()
#     return jsonify([e.serialize() for e in usuarios])
