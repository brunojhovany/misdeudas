from flask_restful import Resource, request
from flask_jwt_extended import jwt_required

from models import entities

class deuda_del_mes(Resource):
    @jwt_required
    def get(self):
        entities.Deuda.get_deudas(request.args['usuario'], 1)
        return {
            'deudas_del_mes': entities.Deuda.get_deudas(request.args['usuario'], 1)
        }
