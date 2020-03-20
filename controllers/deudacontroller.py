from flask_restful import Resource, reqparse
from flask_jwt_extended import jwt_required, get_jwt_identity
from business.usuariobusiness import Usuario_Business

nueva_deuda = reqparse.RequestParser()
nueva_deuda.add_argument('descripcion', help='this field is required', required=True)
nueva_deuda.add_argument('fecha', help='this field is required', required=True)
nueva_deuda.add_argument('fecha_fin', help='this field is required', required=True)
nueva_deuda.add_argument('mensualidades', help='this field is required', required=True)
nueva_deuda.add_argument('total', help='this field is required', required=True)
nueva_deuda.add_argument('id_entidad_bancaria', help='this field is required', required=True)


class Deuda(Resource):
    @jwt_required
    def post(self):
        usr = get_jwt_identity()
        data = nueva_deuda.parse_args()
        return Usuario_Business.Nueva_deuda(usr, data)

    @jwt_required
    def get(self):
        usr = get_jwt_identity()
        return Usuario_Business.deuda_mensual(usr)
