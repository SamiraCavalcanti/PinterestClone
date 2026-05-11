from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager
import os
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DATABASE_URL', 'sqlite:///comunidade.db')
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', 'K7mP2xQ9nL5bJ8vR4sW3yZ1aE6fH0uX')
app.config['UPLOAD_FOLDER'] = 'static/fotos_posts'

database = SQLAlchemy(app)
bcrypt = Bcrypt(app)
login_manager = LoginManager()
login_manager.login_view = 'homepage'
login_manager.init_app(app)

from src.app.models import Usuario

@login_manager.user_loader
def load_usuario(user_id):
    return Usuario.query.get(int(user_id))

from src.app import routes

