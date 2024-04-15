from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from os import path
from flask_login import LoginManager

db = SQLAlchemy()
app = Flask(__name__)
DB_NAME = 'database.db'

def create_app():
    app.config['SECRET_KEY'] = 'dgfodhf-uisdfhfidsf-ehifsdfds-ophbsaiud'
    app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{DB_NAME}'
    db.init_app(app)
    
    from .api import api
    from .views import views
    from .auth import auth
    from .search import search
    
    app.register_blueprint(api, url_prefix='/')
    app.register_blueprint(views, url_prefix='/')
    app.register_blueprint(auth, url_prefix='/')
    app.register_blueprint(search, url_prefix='/')
    
    from .models import User, Playlists
    
    with app.app_context():
        db.create_all()
    
    login_manager = LoginManager()
    login_manager.login_auth = 'auth.login'
    login_manager.init_app(app)
    
    @login_manager.user_loader
    def load_user(id):
        return User.query.get(int(id))
    
    return app

def create_database(app):
    if not path.exists('website/' + DB_NAME):
        db.create_all(app=app)
        print('Created Database!')