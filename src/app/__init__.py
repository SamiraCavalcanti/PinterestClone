from flask import Flask
from  flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///comunidade.db'
app.config['SECRET_KEY'] = 'K7mP2xQ9nL5bJ8vR4sW3yZ1aE6fH0uX'

database = SQLAlchemy(app)
bcrypt = Bcrypt(app)
login_manager = LoginManager()
login_manager.login_view = 'homepage'

from src.app import routes

