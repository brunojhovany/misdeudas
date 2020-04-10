from flask import request
from models.entities import Deuda, Usuario, Mensualidad, Entidad_Bancaria
from datetime import datetime
class Usuario_Business():
    @classmethod
    def Nueva_deuda(cls, nombre_usuario):
        entidad_bancaria = Entidad_Bancaria.find_by_id(request.json['id_entidad_bancaria'])
        next_id_duedaseq = Deuda.get_next_id_from_seq()
        current_user = Usuario.find_by_username(nombre_usuario)
        total = float(request.json['total'])
        mensualidades = request.json['mensualidades']
        nueva_deuda = Deuda(
            id_deuda=next_id_duedaseq,
            descripcion_deuda=request.json['descripcion'],
            fecha_deuda=datetime.strptime(request.json['fecha'], '%Y-%m-%dT%H:%M:%S.%fZ'),
            fecha_fin_deuda=datetime.strptime(request.json['fecha_fin'], '%Y-%m-%dT%H:%M:%S.%fZ'),
            mensualidades=mensualidades,
            total_deuda=total,
            id_estatus=1,
            id_entidad_bancaria=request.json['id_entidad_bancaria'],
            id_usuario=current_user.id_usuario
        )
        if mensualidades:
            nueva_deuda.mensualidades = True
            nueva_deuda.save()
            total_por_mes = total / mensualidades
            return {"Su total a  pagar por mes": total_por_mes}
        else:
            nueva_deuda
            return {"message": ""}

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
