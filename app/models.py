import base64
import os
from app import db, login
from datetime import datetime, timedelta
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(50), nullable=False, unique=True)
    username = db.Column(db.String(50), nullable=False, unique=True)
    password = db.Column(db.String(256), nullable=False)
    date_created = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    token = db.Column(db.String(32), index=True, unique= True)
    token_expiration = db.Column(db.DateTime)

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.set_password(kwargs['password'])
        db.session.add(self)
        db.session.commit()

    def check_password(self, password):
        return check_password_hash(self.password, password)

    def set_password(self,password):
        self.password = generate_password_hash(password)
        db.session.commit()

    def to_dict(self):
        return{
            "id": self.id,
            "email": self.email,
            "username": self.username,
            "date_created": self.date_created,
            "password": self.password
        }
    def get_token(self, expires_in=10000):
        now = datetime.utcnow()
        if self.token and self.token_expiration > now + timedelta(seconds=60):
            return self.token
        self.token = base64.b64encode(os.urandom(24)).decode('utf-8')
        self.token_expiration = now + timedelta(seconds=expires_in)
        db.session.commit()
        return self.token
    
    def revoke_token(self):
        self.token_expiration = datetime.utcnow() - timedelta(seconds=1)
        db.session.commit()
    
@login.user_loader
def load_user(user_id):
    return User.query.get(user_id)

class Shows(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    date = db.Column(db.String(100), nullable=False)
    time = db.Column(db.String(50), nullable=False)
    description = db.Column(db.String(250), nullable =True)   

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        db.session.add(self)
        db.session.commit()
    
    def to_dict(self):
        return{
            "id": self.id,
            "date": self.date,
            "time": self.time,
            "description": self.description
        }

    def delete(self):
        db.session.delete(self)
        db.session.commit()

class Orders(db.Model, UserMixin):
        id = db.Column(db.Integer, primary_key=True)
        items = db.Column(db.String, nullable=False)
        date_created = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
        fuffiled = db.Column(db.Boolean, nullable=False, default=False)
    
        def __init__(self, **kwargs):
            super().__init__(**kwargs)
            db.session.add(self)
            db.session.commit()
        
        def to_dict(self):
            return{
                "id": self.id,
                "items": self.items,
                "date_created": self.date_created,
                "fufilled": self.fuffiled
            }

class Merch(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False)
    price = db.Column(db.String(15), nullable=False, default="9.99")
    img = db.Column(db.BLOB, unique=True, nullable=False)
    mimetype = db.Column(db.Text, nullable=False)

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        db.session.add(self)
        db.session.commit()

    def to_dict(self):
            return{
                "id": self.id,
                "name": self.name,
                "price": self.price,
                "img": self.img,
                "mimetype": self.mimetype
            }
