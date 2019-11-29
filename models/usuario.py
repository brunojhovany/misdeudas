from app import db
# from sqlalchemy import Column, PrimaryKeyConstraint, Integer


class Usuario(db.Model):
    __tablename__ = 'usuario'
    __table_args__ = {"schema": "seguridad"}
    id_usuario = db.Column(db.Integer, primary_key=True)
    nombre_usuario = db.Column(db.String)
    password_usuario = db.Column(db.String)
    salt_usuario = db.Column(db.String)

    def get_id(self):
        return self.nombre_usuario

    def serialize(self):
        return {
            'id_usuario': self.id_usuario,
            'nombre_usuario': self.nombre_usuario,
            'password_usuario': self.password_usuario,
            'salt_usuario': self.salt_usuario
        }
