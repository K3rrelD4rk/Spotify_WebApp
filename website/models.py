from website import db
from flask_login import UserMixin
from sqlalchemy.sql import func
    
class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    Username = db.Column(db.String(150))
    email = db.Column(db.String(150), unique=True)
    password = db.Column(db.String(150), nullable = False)
    playlists = db.relationship('Playlists')

class Playlists(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    pl_name = db.Column(db.String(150))
    creation_date = db.Column(db.DateTime(timezone=True), default=func.now())
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))