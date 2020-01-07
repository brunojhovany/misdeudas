from app import db
# from sqlalchemy import Column, PrimaryKeyConstraint, Integer


class Usuario(db.Model):
    __tablename__ = 'usuario'
    __table_args__ = {"schema": "seguridad"}
    id_usuario = db.Column(db.Integer, primary_key=True)
    nombre_usuario = db.Column(db.String)
    password_usuario = db.Column(db.String)
    salt_usuario = db.Column(db.String)
    id_estatus = db.Column(db.Integer, db.ForeignKey('catalogo.estatus.id_estatus'), nullable=False)

    def get_id(self):
        return self.nombre_usuario

    def serialize(self):
        return {
            'id_usuario': self.id_usuario,
            'nombre_usuario': self.nombre_usuario,
            'password_usuario': self.password_usuario,
            'salt_usuario': self.salt_usuario,
            'id_estatus': self.id_estatus
        }

    def save(self):
        db.session.add(self)
        db.session.commit()

    @classmethod
    def find_by_username(cls, username):
        return cls.query.filter_by(nombre_usuario=username).first()

    @classmethod
    def get_all_usuers(cls):
        usuarios = cls.query.all()
        return {'users': list(map(lambda element: cls.serialize(element), usuarios))}


class Estatus (db.Model):
    __tablename__ = 'estatus'
    __table_args__ = {"schema": "catalogo"}
    id_estatus = db.Column(db.Integer, primary_key=True)
    descripcion_estatus = db.Column(db.String)

    usuarios = db.relationship('Usuario', backref='usuario', lazy=True)
    # entidadesbancarias = db.relationship('Entidad_Bancaria', backref='estatus', lazy=True)

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


class Entidad_Bancaria(db.Model):
    __tablename__ = 'entidad_bancaria'
    __table_args__ = {"schema": "catalogo"}
    id_entidad = db.Column(db.Integer, primary_key=True)
    descripcion_entidad = db.Column(db.String)
    id_estatus = db.Column(db.Integer, db.ForeignKey('catalogo.estatus.id_estatus'), nullable=False)

    def serialize(self):
        return {
            'id_entidad': self.id_entidad,
            'descripcion_entidad': self.descripcion_entidad
        }

    def save(self):
        db.session.add(self)
        db.session.commit()

    @classmethod
    def get_all_estatus(cls):
        estatus = cls.query.all()
        return {'estatus': list(map(lambda element: cls.serialize(element), estatus))}

class RevokedTokenModel(db.Model):
    __tablename__ = 'revoke_token'
    __table_args__ = {"schema": "seguridad"}

    id_revoke_token = db.Column(db.Integer, primary_key=True)
    jti_revoke_token = db.Column(db.String(120))

    def save(self):
        db.session.add(self)
        db.session.commit()

    @classmethod
    def is_jti_blacklisted(cls, jti):
        query = cls.query.filter_by(jti_revoke_token=jti).first()
        return bool(query)
