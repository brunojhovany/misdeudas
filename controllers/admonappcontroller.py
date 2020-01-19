from flask_restful import Resource  # , reqparse
from models import entities
from business.decorators.roldecorator import requiered_admin

# parser = reqparse.RequestParser()
# parser.add_argument('')


class Estatus(Resource):
    @requiered_admin
    def get(self):
        return entities.Estatus.get_all_estatus()

class Entidad_Bancaria(Resource):
    def get(self):
        return entities.Entidad_Bancaria.get_all_entidad_bancaria()
