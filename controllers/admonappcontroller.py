from flask_restful import Resource, reqparse
from models import estatus

# parser = reqparse.RequestParser()
# parser.add_argument('')


class GetEstatus(Resource):
    def get(self):
        return estatus.Estatus.get_all_estatus()
