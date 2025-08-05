from flask_sqlalchemy import SQLAlchemy
from database import db

class Item(db.Model):
    __tablename__ = "items"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100))
    description = db.Column(db.String(200))
    price = db.Column(db.Float)
    in_stock = db.Column(db.Boolean, default=True)