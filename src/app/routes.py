#cria as rotas(links) do site
from flask import Flask, render_template, url_for, redirect
from src.app.models import Usuario, Foto
from src.app import app, database, bcrypt
from flask_login import login_required, login_user,logout_user,current_user
from src.app.forms import FormCriarConta, FormLogin, FormFoto
import os
from werkzeug.utils import secure_filename


#@app  é um decorador que é usado para associar uma função a uma rota específica. Ele é usado para definir as rotas do aplicativo Flask e associá-las a funções que serão executadas quando essas rotas forem acessadas.
@app.route('/', methods=['GET', 'POST'])
def homepage():
    formlogin = FormLogin()
    if formlogin.validate_on_submit():
        usuario = Usuario.query.filter_by(email=formlogin.email.data).first()
        if usuario and bcrypt.check_password_hash(usuario.senha, formlogin.senha.data):
            login_user(usuario)
            return redirect(url_for('perfil', id_usuario=usuario.id))
    return render_template('homepage.html', form=formlogin)

@app.route('/criarconta', methods=['GET', 'POST'])
def criar_conta():
    formcriarconta = FormCriarConta()
    if formcriarconta.validate_on_submit():
         senha = bcrypt.generate_password_hash(formcriarconta.senha.data).decode('utf-8')
         nome = Usuario(nome=formcriarconta.nome.data,
                        email=formcriarconta.email.data, senha=senha  )
         database.session.add(nome)
         database.session.commit()
         login_user(nome, remember=True)
         return redirect(url_for('perfil', id_usuario=nome.nome))
    return render_template('criarconta.html', form=formcriarconta)
 
@app.route('/perfil/<id_usuario>', methods=['GET', 'POST'])
@login_required
def perfil(id_usuario):
    if int(id_usuario) == int(current_user.id):
       form_foto = FormFoto()
       if form_foto.validate_on_submit():
            foto = form_foto.foto.data
            nome_seguro = secure_filename(foto.filename)
            #salvar a foto no diretório de fotos_posts
            caminho_arquivo = os.path.join(os.path.abspath(os.path.dirname(__file__)), app.config['UPLOAD_FOLDER'], nome_seguro)
            
            foto.save(caminho_arquivo)
            #salvar a foto no banco de dados
            foto_usuario = Foto(imagem=nome_seguro, id_usuario=current_user.id)
            database.session.add(foto_usuario)
            database.session.commit()
         
       return render_template('perfil.html', usuario=current_user, form=form_foto)
    else:
        usuario = Usuario.query.get(int(id_usuario))
    return render_template('perfil.html', usuario=usuario,form=None)

@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('homepage'))
