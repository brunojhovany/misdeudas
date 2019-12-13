from app import db


class Estatus (db.Model):
    __tablename__ = 'estatus'
    __table_args__ = {"schema": "catalogo"}
    id_estatus = db.Column(db.Integer, primary_key=True)
    descripcion_estatus = db.Column(db.String)

    def serialize(self):
        return {
            'id_estatus': self.id_estatus,
            'descripcion_estatus': self.descripcion_estatus
        }

    def save(self):
        db.session.add(self)
        db.session.commit()

    @classmethod
    def find_by_id(cls, id_estatus):
        return cls.query.filter_by(id_estatus=id_estatus).first()

    @classmethod
    def get_all_estatus(cls):
        estatus = cls.query.all()
        return {'estatus': list(map(lambda element: cls.serialize(element), estatus))}
