from flask import Flask, render_template, url_for, flash, redirect
from MediFlow import app


@app.route('/home')
def home():
    lista_usuarios = ['João', 'Maria', 'Pedro', 'Ana', 'Carlos']
    return render_template('home.html', lista_usuarios=lista_usuarios)

@app.route('/login')
def login():
    return render_template('login.html')