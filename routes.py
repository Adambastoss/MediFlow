from flask import Flask, render_template, url_for, flash, redirect
from MediFlow import app
from MediFlow.forms import FormLogin 


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




