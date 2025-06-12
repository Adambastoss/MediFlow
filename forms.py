from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, BooleanField
from wtforms.validators import DataRequired, Length

class FormLogin(FlaskForm):
    cpf = StringField('CPF', validators=[DataRequired(), Length(min=11, max=16)])
    senha = PasswordField('Senha', validators=[DataRequired(), Length(min=6, max=20)])
    lembrar_dados = BooleanField('Lembrar dados')
    btn_logar = SubmitField('Entrar')
