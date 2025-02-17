from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(80), unique=False, nullable=False)
    is_active = db.Column(db.Boolean(), unique=False, nullable=False)

    def __repr__(self):
        return '<Usuario %r>' % self.email

    def serialize(self):
        return {
            "id": self.id,
            "email": self.email,
            # do not serialize the password, its a security breach
        }


class Director(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(250), nullable=False)
    nacionalidad = db.Column(db.String(250), nullable=False)
    numero_peliculas = db.Column(db.Integer, nullable=False)
    peliculas = db.relationship('Pelicula', backref='director')

    def __repr__(self):
        return '<Director ' + str(self.id) + self.nombre+ '>'

    def serialize(self):
        return {
            "id": self.id,
            "nombre": self.nombre,
            "num_peliculas": self.numero_peliculas,
            "rate": 5
            # do not serialize the password, its a security breach
        }

class Pelicula(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    titulo = db.Column(db.String(250), nullable=False)
    genero = db.Column(db.String(250), nullable=False)
    duracion = db.Column(db.Integer, nullable=False)
    director_id = db.Column(db.Integer, db.ForeignKey('director.id'))

    def __repr__(self):
        return '<Pelicula %r>' % self.titulo

    def serialize(self):
        return {
            "id": self.id,
            "titulo": self.titulo,
            "genero": self.genero
            # do not serialize the password, its a security breach
        }