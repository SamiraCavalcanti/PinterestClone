"""Inicializa o banco de dados com as tabelas necessárias"""
from src.app import app, database

with app.app_context():
    database.create_all()
    print("✓ Banco de dados criado com sucesso!")
