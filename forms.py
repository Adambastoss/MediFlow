from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, BooleanField
from wtforms.validators import DataRequired, Length, Email, EqualTo # Email não será mais usado no login, mas pode ser útil para outras partes

class FormLogin(FlaskForm):
    # Campo para o CPF, substituindo o e-mail
    # Ajuste o Length(min=11, max=14) conforme o formato de CPF que você armazena (com ou sem máscara)
    cpf = StringField('CPF', validators=[DataRequired(), Length(min=11, max=14, message='CPF inválido. Use 11 dígitos ou o formato com máscara.')])
    
    senha = PasswordField('Senha', validators=[DataRequired(), Length(6, 20, message='A senha deve ter entre 6 e 20 caracteres.')])
    lembrar_dados = BooleanField('Lembrar dados')
    btn_logar = SubmitField('Entrar')