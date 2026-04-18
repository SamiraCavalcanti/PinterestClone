from src.app import database, app
from src.app.models import Usuario, Foto

with app.app_context():
    database.create_all()