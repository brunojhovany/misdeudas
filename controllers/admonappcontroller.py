from flask_restful import Resource  # , reqparse
from models import entities

# parser = reqparse.RequestParser()
# parser.add_argument('')


class GetEstatus(Resource):
    def get(self):
        return entities.Estatus.get_all_estatus()
