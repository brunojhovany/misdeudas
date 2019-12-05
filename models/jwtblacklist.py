from app import db
class RevokedTokenModel(db.Model):
    __tablename__ = 'revoke_token'
    __table_args__ = {"schema": "seguridad"}

    id_revoke_token = db.Column(db.Integer, primary_key=True)
    jti_revoke_token = db.Column(db.String(120))

    def save(self):
        db.session.add(self)
        db.commit()

    @classmethod
    def is_jti_blacklisted(cls, jti):
        query = cls.query.filter_by(jti_revoke_token=jti).first()
        return bool(query)
