#criar estrutura do banco de dados
from src.app import database, login_manager
from datetime import datetime
from flask_login import UserMixin

#função para carregar o usuário logado, usando o id do usuário para buscar no banco de dados e retornar o objeto do usuário correspondente. 
def load_usuario(id_usuario):
    return Usuario.query.get(int(id_usuario))


class Usuario(database.Model, UserMixin):
    id = database.Column(database.Integer, primary_key=True)
    nome = database.Column(database.String(100), nullable=False)
    email = database.Column(database.String(100), unique=True, nullable=False)
    senha = database.Column(database.String(100), nullable=False)
    fotos = database.relationship('Foto', backref='usuario', lazy=True)

    def __repr__(self):
        return f'<Usuario {self.nome}>'
    
class Foto (database.Model):
    id = database.Column(database.Integer, primary_key=True)
    imagem = database.Column(database.String, default='default.png', nullable=False )
    data_criacao = database.Column(database.DateTime, nullable=False, default=datetime.utcnow)
    id_usuario = database.Column(database.Integer, database.ForeignKey('usuario.id'), nullable=False)

    def __repr__(self):
        return f'<Foto {self.imagem}>'