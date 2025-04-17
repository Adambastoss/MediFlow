from flask import Flask, render_template, url_for, flash, redirect, request
from MediFlow import app, db
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
    procedimentos = Procedimentos.query.all()  # Obtendo os procedimentos do banco
    return render_template('procedimentos.html', procedimentos=procedimentos)

@app.route('/procedimentos/editar/<int:id>', methods=['POST'])
def editar_procedimento_modal(id):
    procedimento = Procedimentos.query.get_or_404(id)

    procedimento.nome = request.form['nome']
    procedimento.categoria = request.form['categoria']
    procedimento.preco = request.form['preco']
    procedimento.descricao = request.form['descricao']
    procedimento.ativo = True if request.form.get('ativo') == 'on' else False
    procedimento.tempo_estimado = request.form['tempo_estimado']

    db.session.commit()
    return redirect(url_for('procedimentos'))

@app.route('/procedimentos/excluir/<int:id>', methods=['POST'])
def excluir_procedimento(id):
    procedimento = Procedimentos.query.get_or_404(id)
    db.session.delete(procedimento)
    db.session.commit()
    return redirect(url_for('procedimentos'))

@app.route('/procedimentos/cadastrar', methods=['POST'])
def cadastrar_procedimento():
    nome = request.form['nome']
    categoria = request.form['categoria']
    preco = request.form['preco']
    descricao = request.form['descricao']
    ativo = True if request.form.get('ativo') == 'on' else False
    tempo_estimado = request.form['tempo_estimado']

    novo_procedimento = Procedimentos(
        nome=nome,
        categoria=categoria,
        preco=preco,
        descricao=descricao,
        ativo=ativo,
        tempo_estimado=tempo_estimado
    )

    db.session.add(novo_procedimento)
    db.session.commit()

    return redirect(url_for('procedimentos'))



