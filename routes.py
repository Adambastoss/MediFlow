from flask import Flask, render_template, url_for, flash, redirect
from MediFlow import app


@app.route('/home')
def home():
    return render_template('home.html')

@app.route('/')
def login():
    return render_template('login.html')


