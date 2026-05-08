# criar formulário de cadastro e login
from flask_wtf import FlaskForm
from wtforms import Field, StringField, PasswordField, SubmitField, FileField
from wtforms.validators import DataRequired, Email, Length, EqualTo, ValidationError
from src.app.models import Usuario  


class FormCriarConta(FlaskForm):
    nome = StringField('Nome Completo:', validators=[DataRequired()])
    email = StringField('E-mail:', validators=[DataRequired(), Email()])
    senha = PasswordField('Senha:', validators=[DataRequired(), Length(min=6)])
    confirmar_senha = PasswordField('Confirmar Senha:', validators=[DataRequired(), EqualTo('senha')])
    botao_submit_criar_conta = SubmitField('Criar Conta')

    def validate_email(self, email):
        usuario = Usuario.query.filter_by(email=email.data).first()
        if usuario:
            raise ValidationError('Este email já está em uso.Faça login ou tente outro email.')   

class FormLogin(FlaskForm):
    email = StringField('Email:', validators=[DataRequired(), Email()])
    senha = PasswordField('Senha:', validators=[DataRequired()])
    botao_submit_login = SubmitField('Login')

    def validate_email(self, email):
        usuario = Usuario.query.filter_by(email=email.data).first()
        if not usuario:
            raise ValidationError('Usuário não encontrado. Faça o cadastro ou tente outro email.')   


class FormFoto(FlaskForm):
    foto = FileField('Foto:', validators=[DataRequired()])
    botao_submit_foto = SubmitField('Enviar Foto')