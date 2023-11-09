from management import db
from flask_login import UserMixin
from sqlalchemy.sql import func

class Note(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    data = db.Column(db.String(10000))
    date = db.Column(db.DateTime(timezone=True),default=func.now())
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"))
    

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(150), unique=True)
    password = db.Column(db.String(150))
    user_name = db.Column(db.String(150))
    notes = db.relationship("Note")
    # Thêm quan hệ ngược với bảng Order
    orders = db.relationship("Order", back_populates="user")
    def __init__(self, email, password, user_name):
        self.password: Any
        self.email = email
        self.password = password
        self.user_name = user_name

class Order(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    product_name = db.Column(db.String(255), nullable=False)
    total_price = db.Column(db.Float, nullable=False)

    # Tạo khóa ngoại để liên kết với bảng User
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"))
    
    # Tạo quan hệ với bảng User
    user = db.relationship("User", back_populates="orders")

    def __init__(self, product_name, total_price, user):
        self.product_name = product_name
        self.total_price = total_price
        self.user = user