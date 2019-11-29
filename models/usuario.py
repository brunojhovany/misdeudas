from app import db
# from sqlalchemy import Column, PrimaryKeyConstraint, Integer


class Usuario(db.Model):
    __tablename__ = 'seguridad.usuario'
    id_usuario = db.Column(db.Integer, primary_key=True)
    nombre_usuario = db.Column(db.String)
    password_usuario = db.Column(db.String)
    salt_usuario = db.Column(db.String)

    def get_id(self):
        return self.nombre_usuario
