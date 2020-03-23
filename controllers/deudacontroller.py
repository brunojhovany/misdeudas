from flask_restful import Resource
from flask_jwt_extended import jwt_required, get_jwt_identity
from business.usuariobusiness import Usuario_Business
from business.decorators.schema_validator import validate_schema

class Deuda(Resource):
    @jwt_required
    @validate_schema('nueva_deuda')
    def post(self):
        usr = get_jwt_identity()
        return Usuario_Business.Nueva_deuda(usr)

    @jwt_required
    def get(self):
        usr = get_jwt_identity()
        return Usuario_Business.deuda_mensual(usr)
