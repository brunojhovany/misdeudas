from flask_restful import Resource, reqparse
from models import entities
from util import utilerias
from flask_jwt_extended import (create_access_token, create_refresh_token, jwt_required, jwt_refresh_token_required, get_jwt_identity, get_raw_jwt)
from datetime import timedelta
from business.decorators.roldecorator import requiered_admin

parser = reqparse.RequestParser()
parser.add_argument('username', help='this field is required', required=True)
parser.add_argument('password', help='this field is required', required=True)

class create_dev_token(Resource):
    @requiered_admin
    def post(self):
        data = parser.parse_args()
        current_user = entities.Usuario.find_by_username(data['username'])
        if not current_user:
            return { 'message':'user {} not found'.format(data['username']) }, 404
        if utilerias.Utilerias.matchHashText(current_user.password_usuario, current_user.salt_usuario, data['password']):
            expires = timedelta(days=31)
            access_token = create_access_token(current_user, expires_delta=expires)
            return {
                'message': 'Developer user logged in as {}'.format(data['username']),
                'access_token': access_token
            }, 200
        else:
            return {'message':'password does not match.'}, 401

class UsuarioRegister(Resource):
    def post(self):
        data = parser.parse_args()
        if entities.Usuario.find_by_username(data['username']):
            return {'message': 'user {} alredy exists'.format(data['username'])}, 400

        results = utilerias.Utilerias.hashpassword(data['password'])
        newUser = entities.Usuario(
            nombre_usuario=data['username'],
            password_usuario=results[0],
            salt_usuario=results[1],
            id_estatus=2
        )
        try:
            newUser.save()
            # access_token = create_access_token(identity=data['username'])
            # refresh_token = create_refresh_token(identity=data['username'])
            return {
                'message': 'User {} created please contact the administrator to activate your account'.format(data['username'])
            }
        except NameError:
            return {'message': 'something went wrong'}, 500


class UsuarioLogin(Resource):
    def post(self):
        data = parser.parse_args()
        current_user = entities.Usuario.find_by_username(data['username'])
        if not current_user:
            return {'message': 'User {} doesn\'t exists'.format(data['username'])}

        if utilerias.Utilerias.matchHashText(
                current_user.password_usuario, current_user.salt_usuario, data['password']):
            access_token = create_access_token(current_user)
            refresh_token = create_refresh_token(current_user)
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
            revoked_token = entities.RevokedTokenModel(jti_revoke_token=jti)
            revoked_token.save()
            return {'message': 'Access token has been revoked'}
        except NameError:
            return {'message': 'something went wrong'}, 500


class UsuarioLogoutRefresh(Resource):
    @jwt_refresh_token_required
    def post(self):
        jti = get_raw_jwt()['jti']
        try:
            revoked_token = entities.RevokedTokenModel(jti_revoke_token=jti)
            revoked_token.save()
            return {'message': 'Refresh token has been revoked'}
        except NameError:
            return {'message': 'something went wrong'}, 500


class TokenRefresh(Resource):
    @jwt_refresh_token_required
    def post(self):
        current_user = get_jwt_identity()
        current_user = entities.Usuario.find_by_username(current_user)
        access_token = create_access_token(current_user)
        return {'access_token': access_token}


class AllUsers(Resource):
    def get(self):
        return entities.Usuario.get_all_usuers()


class TestSecurity(Resource):
    @jwt_required
    def post(self):
        return {'message': 420}
