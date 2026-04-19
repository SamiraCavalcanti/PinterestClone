#cria as rotas(links) do site
from flask import Flask, render_template, url_for
from src.app import app
from flask_login import login_required, current_user


#@app  é um decorador que é usado para associar uma função a uma rota específica. Ele é usado para definir as rotas do aplicativo Flask e associá-las a funções que serão executadas quando essas rotas forem acessadas.
@app.route('/')
def homepage():
    return render_template('homepage.html')
 
@app.route('/perfil/<usuario>')
@login_required
def perfil(usuario):
    return render_template('perfil.html', usuario=usuario)
