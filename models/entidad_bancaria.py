from app import db


class Entidad_Bancaria(db.Model):
    __tablename__ = 'entidad_bancaria'
    __table_args__ = {"schema": "catalogo"}
    id_entidad = db.Column(db.Integer, primary_key=True)
    descripcion_entidad = db.Column(db.String)
    
