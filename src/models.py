from flask_sqlalchemy import SQLAlchemy


db = SQLAlchemy()


class Users(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(80), unique=False, nullable=False)
    is_active = db.Column(db.Boolean(), unique=False, nullable=False)
    role = db.Column(db.Enum('Jedi', 'Sith', name='role'),nullable=False)

    def __repr__(self):
        return f'<User {self.id} - {self.email}>'

    def serialize(self):
        # do not serialize the password, its a security breach
        return {
            "id": self.id,
            "email": self.email,
            'pass': self.password,
            'is_active': self.is_active,
            'role': self.role}


class Planet(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120), unique=True, nullable=False)
    is_favorite = db.Column(db.Boolean(), unique=False, nullable=False)

    def __repr__(self):
        return '<Planet %r>' % self.id

    def serialize(self):
        # do not serialize the password, its a security breach
        return {
            "id": self.id,
            "name": self.name,
            'is_favorite': self.is_favorite}

class People(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(120), unique=True, nullable=False)
    last_name = db.Column(db.String(120), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    is_favorite = db.Column(db.Boolean(), unique=False, nullable=False)

    def __repr__(self):
        return '<People %r>' % self.id

    def serialize(self):
        # do not serialize the password, its a security breach
        return {
            "id": self.id,
            "firstname": self.first_name,
            "lastname": self.last_name,
            "email": self.email,
            'is_favorite': self.is_favorite}