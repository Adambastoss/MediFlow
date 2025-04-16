from flask import Flask, render_template, url_for, flash, redirect
from MediFlow import app
from MediFlow.forms import FormLogin
from MediFlow.models import Procedimentos


@app.route('/', methods=['POST', 'GET'])
def login():
    form_login = FormLogin()
    if form_login.validate_on_submit():
        flash('Login realizado com sucesso', 'alert-success')
        return redirect(url_for('home'))
    return render_template('login.html', form_login=form_login)


@app.route('/home')
def home():
    return render_template('home.html')

@app.route('/pacientes')
def pacientes():
    return render_template('pacientes.html')

@app.route('/consultas')
def consultas():
    return render_template('consultas.html')

@app.route('/funcionarios')
def funcionarios():
    return render_template('funcionarios.html')
    
@app.route('/procedimentos')
def procedimentos():
    return render_template('procedimentos.html')



