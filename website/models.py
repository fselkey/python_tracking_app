from . import db
from flask_login import UserMixin
from sqlalchemy.sql import func

class Note(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    data = db.Column(db.String(10000))
    date = db.Column(db.DateTime(timezone=True), default=func.now())


class Order(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    po_num = db.Column(db.String(10000))
    so_num = db.Column(db.String(10000))
    date = db.Column(db.DateTime(timezone=True), default=func.now())

class Track(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    order_id = db.Column(db.Integer, db.ForeignKey('order.id'))
    received = db.Column(db.Boolean)
    tested = db.Column(db.Boolean)
    shipped = db.Column(db.Boolean)
    location = db.Column(db.String(10000))
    last_update = db.Column(db.DateTime(timezone=True), default=func.now())
    orders = db.relationship('Order')

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(150), unique=True)
    password = db.Column(db.String(150))
    first_name = db.Column(db.String(150))
    notes = db.relationship('Note')
    orders = db.relationship('Order')
    tracks = db.relationship('Track')