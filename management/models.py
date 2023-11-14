from management import db
from flask_login import UserMixin
from sqlalchemy.sql import func
from sqlalchemy import DECIMAL
from sqlalchemy.orm import relationship
from datetime import datetime 
from sqlalchemy import LargeBinary
class Note(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    data = db.Column(db.String(10000))
    date = db.Column(db.DateTime(timezone=True), default=func.now())
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"))

class Product(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), nullable=False)
    total_price = db.Column(db.DECIMAL(precision=12, scale=2)) 
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(150), unique=True)
    password = db.Column(db.String(150))
    user_name = db.Column(db.String(150))
    notes = db.relationship("Note")

    products = db.relationship("Product")
    def __init__(self, email, password, user_name):
        self.email = email
        self.password = password
        self.user_name = user_name
class Order(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(255))
    last_name = db.Column(db.String(255))
    email = db.Column(db.String(255))
    phone_number = db.Column(db.String(20))
    address = db.Column(db.String(255))
    city = db.Column(db.String(100))
    state = db.Column(db.String(100))
    zip_code = db.Column(db.String(10))
    payment_method = db.Column(db.String(50), nullable=False)
    total_price = db.Column(db.Float, nullable=False)
    __tablename__ = 'order'
class Admin(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    admin_name = db.Column(db.String(150))
    password = db.Column(db.String(150))
    def __init__(self, admin_name, password):
        self.admin_name = admin_name
        self.password = password
        __tablename__ = 'admin'

class Amin_addProduct(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    productName = db.Column(db.String(255), nullable=False, name='productName') 
    quantity = db.Column(db.Integer, nullable=False)
    price = db.Column(db.Float, nullable=False)
    image = db.Column(db.String(255))

    def __repr__(self):
        return f'<Product {self.productName}>'
