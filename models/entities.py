from app import db
from datetime import date, datetime


class Usuario(db.Model):
    __tablename__ = 'usuario'
    __table_args__ = {"schema": "seguridad"}
    id_usuario = db.Column(db.Integer, primary_key=True)
    nombre_usuario = db.Column(db.String(80))
    password_usuario = db.Column(db.String(150))
    salt_usuario = db.Column(db.String(80))
    id_estatus = db.Column(db.Integer, db.ForeignKey('catalogo.estatus.id_estatus'), nullable=False)

    deuda = db.relationship('Deuda', backref='usuario', lazy='dynamic')
    roles = db.relationship('Rol_Por_Usuario', backref='rol_por_usuario', lazy=True)

    def get_id(self):
        return self.nombre_usuario

    def serialize(self):
        return {
            'id_usuario': self.id_usuario,
            'nombre_usuario': self.nombre_usuario,
            # 'password_usuario': self.password_usuario,
            # 'salt_usuario': self.salt_usuario,
            'estatus': Estatus.serialize(self.estatus)
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
    descripcion_estatus = db.Column(db.String(40))

    usuarios = db.relationship('Usuario', backref='estatus', lazy='dynamic')
    entidadesbancarias = db.relationship('Entidad_Bancaria', backref='estatus', lazy='dynamic')
    deudas = db.relationship('Deuda', backref='estatus', lazy='dynamic')
    mensualidades = db.relationship('Mensualidad', backref='estatus', lazy='dynamic')
    rolporusario = db.relationship('Rol_Por_Usuario', backref='rpu', lazy='dynamic')

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
    id_entidad_bancaria = db.Column(db.Integer, primary_key=True)
    descripcion_entidad = db.Column(db.String(40))
    id_estatus = db.Column(db.Integer, db.ForeignKey('catalogo.estatus.id_estatus'), nullable=False)

    deudas = db.relationship('Deuda', backref='entidad_bancaria', lazy='dynamic')

    def serialize(self):
        return {
            'id_entidad': self.id_entidad_bancaria,
            'descripcion_entidad': self.descripcion_entidad,
            'estatus': Estatus.serialize(self.estatus)
        }

    def save(self):
        db.session.add(self)
        db.session.commit()

    @classmethod
    def get_all_entidad_bancaria(cls):
        entidadesbancarias = cls.query.all()
        return {'bancos': list(map(lambda element: cls.serialize(element), entidadesbancarias))}

class Deuda(db.Model):
    __tablename__ = 'deuda'
    __table_args__ = {'schema': 'persona'}
    id_deuda = db.Column(db.Integer, primary_key=True)
    descripcion_deuda = db.Column(db.String(80))
    fecha_deuda = db.Column(db.DateTime)
    fecha_fin_deuda = db.Column(db.Date)
    mensualidades = db.Column(db.Boolean)
    total_deuda = db.Column(db.Float, nullable=False)
    id_estatus = db.Column(db.Integer, db.ForeignKey('catalogo.estatus.id_estatus'), nullable=False)
    id_entidad_bancaria = db.Column(db.Integer, db.ForeignKey('catalogo.entidad_bancaria.id_entidad_bancaria'), nullable=False)
    id_usuario = db.Column(db.Integer, db.ForeignKey('seguridad.usuario.id_usuario'), nullable=False)

    _mensualidades = db.relationship('Mensualidad', backref='deuda', lazy='dynamic')

    def save(self):
        db.session.add(self)
        db.session.commit()

    def serialize(self):
        return {
            'id_deuda': self.id_deuda,
            'descripcion_deuda': self.descripcion_deuda,
            'fecha_deuda': "%s" % self.json_serial(self.fecha_deuda),
            'fecha_fin_deuda': "%s" % self.json_serial(self.fecha_fin_deuda),
            'mensualidades': self.mensualidades,
            'total_deuda': '%s' % self.total_deuda,
            'estatus': Estatus.serialize(self.estatus),
            'entidad_bancaria': Entidad_Bancaria.serialize(self.entidad_bancaria),
            'usuario': Usuario.serialize(self.usuario)
        }

    def json_serial(self, obj):
        if isinstance(obj, (datetime, date)):
            return obj.isoformat().__str__()
        return ''

    @classmethod
    def get_deudas(cls, id_usuario, id_estatus):
        deudas = cls.query.filter_by(id_usuario=id_usuario, id_estatus=id_estatus)
        return {'deudas': list(map(lambda element: cls.serialize(element), deudas))}


class Mensualidad(db.Model):
    __tablename__ = 'mensualidad'
    __table_args__ = {"schema": "persona"}
    id_deuda = db.Column(db.Integer, db.ForeignKey('persona.deuda.id_deuda'), primary_key=True)
    id_pago = db.Column(db.Integer, primary_key=True)
    id_usuario = db.Column(db.Integer, db.ForeignKey('seguridad.usuario.id_usuario'), nullable=False)
    fecha_pago = db.Column(db.Date)
    id_estatus = db.Column(db.Integer, db.ForeignKey('catalogo.estatus.id_estatus'), nullable=False)
    monto_mensualidad = db.Column(db.Float)


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

class Rol(db.Model):
    __tablename__ = 'rol'
    __table_args__ = {"schema": "catalogo"}
    id_rol = db.Column(db.Integer, primary_key=True)
    descripcion_rol = db.Column(db.String(40), nullable=False)

    rolporusario = db.relationship('Rol_Por_Usuario', backref='rol_porusuario', lazy='dynamic')


class Rol_Por_Usuario(db.Model):
    __tablename__ = 'rol_por_usuario'
    __table_args__ = {"schema": "seguridad"}
    id_rol = db.Column(db.Integer, db.ForeignKey('catalogo.rol.id_rol'), primary_key=True)
    id_usuario = db.Column(db.Integer, db.ForeignKey('seguridad.usuario.id_usuario'), primary_key=True)
    id_estatus = db.Column(db.Integer, db.ForeignKey('catalogo.estatus.id_estatus'), nullable=False)

    def __id(self):
        return self.id_rol

    @classmethod
    def get_roles(cls, rol_por_usuario):
        return list(map(lambda element: cls.__id(element), rol_por_usuario))
