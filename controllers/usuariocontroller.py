from flask_restful import Resource, reqparse
from models import usuario
from flask import jsonify
from util import utilerias


parser = reqparse.RequestParser()
parser.add_argument('username', help='this field is required', required=True)
parser.add_argument('password', help='this field is required', required=True)


class UsuarioRegister(Resource):
    def post(self):
        data = parser.parse_args()
        results = utilerias.Utilerias.hashpassword(data['password'])
        newUser = usuario.Usuario(
            nombre_usuario=data['username'],
            password_usuario=results[0],
            salt_usuario=results[1]
        )
        try:
            newUser.save()
            return {'message': 'User {} was created'.format(data['username'])}
        except NameError:
            return {'message': 'something went wrong'}, 500


class UsuarioLogin(Resource):
    def post(self):
        data = parser.parse_args()
        return data


class UsuarioLogout(Resource):
    def post(self):
        return {'message': 'User logout!'}


class TokenRefresh(Resource):
    def post(self):
        return {'message': 'Refresh Token'}


class AllUsers(Resource):
    def get(self):
        usuarios = usuario.Usuario.query.all()
        return jsonify([e.serialize() for e in usuarios])


class TestSecurity(Resource):
    def post(self):
        return {'message': 420}
