# FakePinterest

Plataforma de compartilhamento de imagens inspirada no Pinterest, desenvolvida com Flask como aplicação fullstack. O projeto inclui autenticação de usuários, upload de fotos, feed personalizado e suite completa de testes automatizados com pipeline CI/CD integrado ao GitHub Actions.

## Pré-requisitos

- Python 3.12 ou superior
- pip (gerenciador de pacotes Python)
- Docker (opcional, para containerização)
- Git

## Instalação Local

### Passo 1: Clonar o repositório

```bash
git clone git@github.com:SamiraCavalcanti/PinterestClone.git
cd PinterestClone
```

### Passo 2: Criar e ativar ambiente virtual

Para Linux/Mac:

```bash
python -m venv venv
source venv/bin/activate
```

Para Windows:

```bash
python -m venv venv
venv\Scripts\activate
```

### Passo 3: Instalar dependências

```bash
pip install --upgrade pip
pip install -r requirements.txt
```

### Passo 4: Executar a aplicação

```bash
python main.py
```

A aplicação estará disponível em http://localhost:5000

## Estrutura do Projeto

```
fakepinterest/
├── .github/
│   └── workflows/
│       ├── ci.yml              # Pipeline de integração contínua
│       └── cd.yml              # Pipeline de entrega contínua
├── src/
│   └── app/
│       ├── __init__.py         # Inicialização da aplicação Flask
│       ├── models.py           # Modelos do banco de dados
│       ├── forms.py            # Formulários WTForms
│       ├── routes.py           # Rotas da aplicação
│       ├── templates/          # Templates HTML
│       │   ├── homepage.html
│       │   ├── criarconta.html
│       │   ├── perfil.html
│       │   ├── feed.html
│       │   └── navbar.html
│       └── static/
│           ├── css/            # Arquivos CSS
│           └── fotos_posts/    # Diretório para uploads
├── tests/
│   └── test_app.py             # Testes automatizados (pytest)
├── conftest.py                 # Configuração pytest
├── main.py                     # Ponto de entrada da aplicação
├── Dockerfile                  # Configuração para containerização
├── .dockerignore               # Arquivos ignorados ao buildar Docker
├── requirements.txt            # Dependências Python
├── .gitignore                  # Arquivos ignorados pelo Git
├── LICENSE                     # Licença MIT
└── README.md                   # Este arquivo
```

## Recursos Principais

Autenticação e Conta de Usuário

- Registro de novos usuários com validação de email
- Login com autenticação segura (bcrypt)
- Senha criptografada no banco de dados
- Sessão persistente com flask-login

Gerenciamento de Fotos

- Upload de fotos para perfil de usuário
- Armazenamento seguro em diretório estático
- Listagem de fotos por usuário
- Visualização de fotos no feed

Feed Social

- Exibição de todas as fotos em ordem cronológica inversa
- Apenas usuários autenticados podem acessar
- Atualização dinâmica do feed

Segurança

- Validação de entrada com WTForms
- Proteção contra CSRF
- Senhas criptografadas com bcrypt
- Rotas protegidas com login_required

## Usando a Aplicação

Funcionalidades de Usuário

1. Criar Conta: Acesse http://localhost:5000/criarconta e preencha o formulário
2. Fazer Login: Volte à página inicial e insira suas credenciais
3. Acessar Perfil: Após login, você será redirecionado para seu perfil
4. Upload de Foto: Na página de perfil, clique em "Escolher Arquivo" e selecione uma imagem
5. Ver Feed: Clique em "Feed" para visualizar todas as fotos da plataforma
6. Logout: Clique em "Sair" para fazer logout

## Testes Automatizados

Executar todos os testes:

```bash
pytest tests/ -v
```

Executar com cobertura de código:

```bash
pytest tests/ -v --cov=src --cov-report=html
```

Suite de Testes

- test_homepage: Verifica se página inicial carrega corretamente
- test_criar_conta: Testa criação de nova conta de usuário
- test_feed_sem_login: Verifica se feed exige autenticação
- test_login_invalido: Testa rejeição de credenciais incorretas
- test_login_valido: Testa login bem-sucedido
- test_feed_com_login: Testa acesso ao feed após autenticação
- test_logout: Testa logout da aplicação

## Usando Docker

Build da imagem Docker:

```bash
docker build -t fakepinterest:latest .
```

Executar a aplicação em container:

```bash
docker run -p 5000:5000 fakepinterest:latest
```

Verificar logs do container:

```bash
docker logs <container-id>
```

Parar o container:

```bash
docker stop <container-id>
```

## Pipeline de CI/CD

Integração Contínua (CI)

O arquivo .github/workflows/ci.yml configura automação para:

- Executar em: Push para main/develop e Pull Requests
- Testa: Código com pytest
- Valida: Sintaxe com flake8
- Gera: Relatório de cobertura
- Upload: Resultados dos testes como artifact

Entrega Contínua (CD)

O arquivo .github/workflows/cd.yml configura automação para:

- Executar em: Push para branch main
- Build: Imagem Docker otimizada
- Push: Para Docker Hub e GitHub Container Registry
- Cache: Otimizado para builds rápidos

Configuração de Secrets

Para ativar o CD (deploy Docker), configure em GitHub:

1. Vá para Settings > Secrets and variables > Actions
2. Adicione novo secret: DOCKER_USERNAME
3. Adicione novo secret: DOCKER_PASSWORD
4. Use suas credenciais do Docker Hub

## Deploy no Kubernetes

Preparação para Kubernetes

A aplicação está pronta para deployment no Kubernetes com:

- Dockerfile otimizado com multi-stage build
- Healthcheck configurado para liveness probe
- Variáveis de ambiente personalizáveis
- Port 5000 exposta

Exemplo de Deployment Kubernetes:

```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: fakepinterest
spec:
  replicas: 2
  selector:
    matchLabels:
      app: fakepinterest
  template:
    metadata:
      labels:
        app: fakepinterest
    spec:
      containers:
        - name: fakepinterest
          image: docker.io/seu-usuario/fakepinterest:latest
          ports:
            - containerPort: 5000
          env:
            - name: FLASK_ENV
              value: production
          livenessProbe:
            httpGet:
              path: /
              port: 5000
            initialDelaySeconds: 10
            periodSeconds: 30
---
apiVersion: v1
kind: Service
metadata:
  name: fakepinterest-service
spec:
  selector:
    app: fakepinterest
  ports:
    - protocol: TCP
      port: 80
      targetPort: 5000
  type: LoadBalancer
```

Aplicar no cluster:

```bash
kubectl apply -f deployment.yaml
```

## Variáveis de Ambiente

A aplicação usa as seguintes variáveis de ambiente:

```
FLASK_APP=main.py              # Arquivo principal da aplicação
FLASK_ENV=production           # Ambiente (production/development)
PYTHONUNBUFFERED=1            # Logs em tempo real no Docker
DATABASE_URL=sqlite:///...    # URL do banco de dados (opcional)
```

## Dependências Principais

- Flask 3.1.3: Framework web
- Flask-SQLAlchemy 3.1.1: ORM para banco de dados
- Flask-Login 0.6.3: Gerenciamento de sessão de usuários
- Flask-Bcrypt 1.0.1: Criptografia de senhas
- Flask-WTF 1.2.1: Processamento de formulários
- pytest 7.4.4: Framework de testes
- python-dotenv 1.0.0: Gerenciamento de variáveis de ambiente

Veja requirements.txt para a lista completa.

## Troubleshooting

Problema: ModuleNotFoundError ao rodar a aplicação

Solução: Certifique-se de que o venv está ativado e conftest.py está na raiz do projeto

Problema: Porta 5000 já está em uso

Solução: Use outra porta com flask run --port 5001

Problema: Banco de dados não encontrado

Solução: Execute conftest.py ou delete instance/comunidade.db para recriá-lo

Problema: Arquivo de foto não é encontrado após upload

Solução: Verifique permissões da pasta static/fotos_posts/ com chmod 755

## Contribuições

Para contribuir ao projeto:

1. Faça um fork do repositório
2. Crie uma branch para sua feature (git checkout -b feature/nova-funcionalidade)
3. Commit suas mudanças (git commit -am 'Adiciona nova funcionalidade')
4. Push para a branch (git push origin feature/nova-funcionalidade)
5. Abra um Pull Request

Padrões de Código

- Siga PEP 8 para Python
- Adicione testes para novas funcionalidades
- Mantenha a documentação atualizada
- Use commits significativos

## Licença

Este projeto está licenciado sob a licença MIT. Veja o arquivo LICENSE para detalhes completos.
