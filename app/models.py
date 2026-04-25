from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class Portafolio(db.Model):
    __tablename__ = 'portafolios'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    nombre = db.Column(db.String(100), nullable=False)
    descripcion = db.Column(db.String(255))
    created_at = db.Column(db.DateTime, default=db.func.current_timestamp())

    favoritos = db.relationship('Favorito', backref='portafolio', lazy=True, cascade='all, delete-orphan')

class Favorito(db.Model):
    __tablename__ = 'favoritos'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    portafolio_id = db.Column(db.Integer, db.ForeignKey('portafolios.id'), nullable=False)
    simbolo = db.Column(db.String(10), nullable=False)
    nombreEmpresa = db.Column(db.String(120))
    added_at = db.Column(db.DateTime, default=db.func.current_timestamp())

    __table_args__ = (db.UniqueConstraint('portafolio_id', 'simbolo', name='unique_portfolio_stock'),)
