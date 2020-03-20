from flask import request
from models.entities import Deuda, Usuario, Mensualidad
class Usuario_Business():
    @classmethod
    def Nueva_deuda(cls, nombre_usuario, data):
        mensualidades = request.json['mensualidades']
        if mensualidades:
            
        return ''

    @classmethod
    def deuda_mensual(cls, nombre_usuario):
        usuario = Usuario.find_by_username(nombre_usuario)
        deudas = Deuda.get_deudas_by_id_usuario(usuario.id_usuario)
        return deudas

    @classmethod
    def deuda_mensual_totla(cls, nombre_usuario):
        usr = Usuario.find_by_username(nombre_usuario)
        deudas = Deuda.get_deudas_by_id_usuario(id_usuario=usr.id_usuario, serializable=False)

        # Hay que sustraer las deudas a meses y las deudas para liquidar en la mensualidad a demas identificarlos}
        # a demas sumar la cantidad total, tambien seria muy bueno crear a partados para identificar con etiquetas
        # a las deudas.
