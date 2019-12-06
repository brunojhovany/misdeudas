from flask_restful import Resource, reqparse
from models import usuario, jwtblacklist
# from flask import jsonify
from util import utilerias
from flask_jwt_extended import (create_access_token, create_refresh_token, jwt_required, jwt_refresh_token_required, get_jwt_identity, get_raw_jwt)

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
            access_token = create_access_token(identity=data['username'])
            refresh_token = create_refresh_token(identity=data['username'])
            return {
                'message': 'User {} was created'.format(data['username']),
                'access_token': access_token,
                'refresh_token': refresh_token
            }
        except NameError:
            return {'message': 'something went wrong'}, 500


class UsuarioLogin(Resource):
    def post(self):
        data = parser.parse_args()
        current_user = usuario.Usuario.find_by_username(data['username'])
        if not current_user:
            return {'message': 'User {} doesn\'t exists'.format(data['username'])}

        if utilerias.Utilerias.matchHashText(
                current_user.password_usuario, current_user.salt_usuario, data['password']):
            access_token = create_access_token(identity=data['username'])
            refresh_token = create_refresh_token(identity=data['username'])
            return {
                'message': 'user logged in as {}'.format(data['username']),
                'access_token': access_token,
                'refresh_token': refresh_token
            }
        else:
            return {'message': 'credentials diden\'t match'}


class UsuarioLogout(Resource):
    @jwt_required
    def post(self):
        jti = get_raw_jwt()['jti']
        try:
            revoked_token = jwtblacklist.RevokedTokenModel(jti_revoke_token=jti)
            revoked_token.save()
            return {'message': 'Access token has been revoked'}
        except NameError:
            return {'message': 'something went wrong'}, 500


class UsuarioLogoutRefresh(Resource):
    @jwt_refresh_token_required
    def post(self):
        jti = get_raw_jwt()['jti']
        try:
            revoked_token = jwtblacklist.RevokedTokenModel(jti_revoke_token=jti)
            revoked_token.save()
            return {'message': 'Refresh token has been revoked'}
        except NameError:
            return {'message': 'something went wrong'}, 500


class TokenRefresh(Resource):
    @jwt_refresh_token_required
    def post(self):
        current_user = get_jwt_identity()
        access_token = create_access_token(identity=current_user)
        return {'access_token': access_token}


class AllUsers(Resource):
    def get(self):
        return usuario.Usuario.get_all_usuers()
        # usuarios = usuario.Usuario.query.all()
        # return jsonify([e.serialize() for e in usuarios])


class TestSecurity(Resource):
    @jwt_required
    def post(self):
        return {'message': 420}
