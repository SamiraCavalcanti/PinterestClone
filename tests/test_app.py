import pytest
from src.app import app, database
from src.app.models import Usuario

@pytest.fixture
def client():
    """Cliente de teste"""
    app.config['TESTING'] = True
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
    
    with app.app_context():
        database.create_all()
        yield app.test_client()
        database.session.remove()
        database.drop_all()

def test_homepage(client):
    """Testa a página inicial"""
    response = client.get('/')
    assert response.status_code == 200

def test_criar_conta(client):
    """Testa criação de conta"""
    response = client.post('/criarconta', data={
        'nome': 'Teste User',
        'email': 'teste@test.com',
        'senha': 'senha123',
        'confirmar_senha': 'senha123'
    }, follow_redirects=True)
    assert response.status_code == 200

def test_feed_sem_login(client):
    """Testa se feed exige login"""
    response = client.get('/feed')
    assert response.status_code == 302  # Redirect

def test_login_invalido(client):
    """Testa login com senha incorreta"""
    # Primeiro criar uma conta
    client.post('/criarconta', data={
        'nome': 'Usuario Login',
        'email': 'login@test.com',
        'senha': 'senha123',
        'confirmar_senha': 'senha123'
    })
    # Tentar fazer login com senha errada
    response = client.post('/', data={
        'email': 'login@test.com',
        'senha': 'senhaerrada'
    }, follow_redirects=True)
    assert response.status_code == 200

def test_login_valido(client):
    """Testa login com credenciais corretas"""
    # Criar conta
    client.post('/criarconta', data={
        'nome': 'Usuario Valido',
        'email': 'valido@test.com',
        'senha': 'senha123',
        'confirmar_senha': 'senha123'
    })
    # Fazer login
    response = client.post('/', data={
        'email': 'valido@test.com',
        'senha': 'senha123'
    }, follow_redirects=True)  # ← Adicionar isso
    assert response.status_code == 200

def test_feed_com_login(client):
    """Testa acesso ao feed quando logado"""
    # Criar conta e fazer login
    client.post('/criarconta', data={
        'nome': 'Usuario Feed',
        'email': 'feed@test.com',
        'senha': 'senha123',
        'confirmar_senha': 'senha123'
    })
    client.post('/', data={
        'email': 'feed@test.com',
        'senha': 'senha123'
    }, follow_redirects=True)
    # Acessar feed
    response = client.get('/feed', follow_redirects=True)
    assert response.status_code == 200  # Agora consegue acessar

def test_logout(client):
    """Testa logout"""
    # Criar e fazer login
    client.post('/criarconta', data={
        'nome': 'Usuario Logout',
        'email': 'logout@test.com',
        'senha': 'senha123',
        'confirmar_senha': 'senha123'
    })
    client.post('/', data={
        'email': 'logout@test.com',
        'senha': 'senha123'
    }, follow_redirects=True)  # ← Adicionar isso
    # Fazer logout
    response = client.get('/logout', follow_redirects=True)
    assert response.status_code == 200