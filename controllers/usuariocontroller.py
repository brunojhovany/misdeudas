from flask_restful import Resource, reqparse
from models import usuario
# from flask import jsonify
from util import utilerias


parser = reqparse.RequestParser()
parser.add_argument('username', help='this field is required', required=True)
parser.add_argument('password', help='this field is required', required=True)


class UsuarioRegister(Resource):
    def post(self):
        data = parser.parse_args()
        if usuario.Usuario.find_by_username(data['username']):
            return {'message': 'user {} alredy exists'.format(data['username'])}, 400

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
        current_user = usuario.Usuario.find_by_username(data['username'])
        if not current_user:
            return {'message': 'User {} doesn\'t exists'.format(data['username'])}

        ismachhash = utilerias.Utilerias.matchHashText(
            current_user.password_usuario, current_user.salt_usuario, data['password'])

        if ismachhash:
            return {'message': 'user {} is logged'.format(data['username'])}
        else:
            return {'message': 'credentials diden\'t match'}


class UsuarioLogout(Resource):
    def post(self):
        return {'message': 'User logout!'}


class TokenRefresh(Resource):
    def post(self):
        return {'message': 'Refresh Token'}


class AllUsers(Resource):
    def get(self):
        return usuario.Usuario.get_all_usuers()
        # usuarios = usuario.Usuario.query.all()
        # return jsonify([e.serialize() for e in usuarios])


class TestSecurity(Resource):
    def post(self):
        return {'message': 420}
