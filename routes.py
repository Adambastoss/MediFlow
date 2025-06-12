from flask import Flask, render_template, url_for, flash, redirect, request, session
from MediFlow import app, db
from MediFlow.forms import FormLogin
from MediFlow.models import Procedimentos, Pacientes, EnderecoPacientes, TelefonePacientes, Funcionarios, EnderecoFuncionarios, TelefoneFuncionarios, Perfis
from werkzeug.security import generate_password_hash, check_password_hash
from functools import wraps
from flask_login import login_required, current_user, login_user, logout_user

@app.route('/', methods=['GET', 'POST'])
def login():
    form_login = FormLogin()
    if form_login.validate_on_submit():
        funcionario = Funcionarios.query.filter_by(cpf=form_login.cpf.data).first()
        if funcionario and check_password_hash(funcionario.senha_hash, form_login.senha.data):
            # Limpa mensagens flash anteriores (ex: logout)
            session.pop('_flashes', None)

            login_user(funcionario, remember=form_login.lembrar_dados.data)
            flash('Login realizado com sucesso!', 'alert-success')
            return redirect(url_for('home'))
        else:
            flash('CPF ou senha incorretos.', 'alert-danger')
    return render_template('login.html', form_login=form_login)


@app.route('/logout')
@login_required
def logout():
    logout_user()
    flash('Logout realizado com sucesso.', 'alert-success')
    return redirect(url_for('login'))

def login_requerido(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'id_funcionario' not in session:
            flash('Faça login para acessar esta página.', 'warning')
            return redirect(url_for('login'))
        return f(*args, **kwargs)
    return decorated_function

def acesso_admin(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if session.get('perfil') != 'ADMIN':
            flash('Acesso negado.', 'danger')
            return redirect(url_for('home'))
        return f(*args, **kwargs)
    return decorated_function

@app.route('/home')
@login_required
def home():
    return render_template('home.html')


@app.route('/consultas')
@login_required
def consultas():
    return render_template('consultas.html')


################################################## PROCEDIMENTOS   
@app.route('/procedimentos')
@login_required
def procedimentos():
    procedimentos = Procedimentos.query.all() 
    return render_template('procedimentos.html', procedimentos=procedimentos)

@app.route('/procedimentos/editar/<int:id>', methods=['POST'])
@login_required
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
@login_required
def excluir_procedimento(id):
    procedimento = Procedimentos.query.get_or_404(id)
    db.session.delete(procedimento)
    db.session.commit()
    return redirect(url_for('procedimentos'))

@app.route('/procedimentos/cadastrar', methods=['POST'])
@login_required
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

################################################## PACIENTES
@app.route('/pacientes')
@login_required
def pacientes():
    pacientes = Pacientes.query.all()
    return render_template('pacientes.html', pacientes=pacientes)

@app.route('/pacientes/cadastrar', methods=['POST'])
@login_required
def cadastrar_paciente():
    nome = request.form['nome']
    cpf = request.form['cpf']
    sexo = request.form['sexo']
    email = request.form.get('email')
    data_nasc = request.form.get('data_nasc')
    observacoes = request.form.get('observacoes')

    novo_paciente = Pacientes(
        nome=nome,
        cpf=cpf,
        sexo=sexo,
        email=email,
        data_nasc=data_nasc,
        observacoes=observacoes
    )
    db.session.add(novo_paciente)
    db.session.commit()

    # Agora cadastra o endereço e o telefone
    endereco = EnderecoPacientes(
        bairro=request.form['bairro'],
        rua=request.form['rua'],
        numero=request.form['numero'],
        cidade=request.form['cidade'],
        uf=request.form['uf'],
        id_paciente=novo_paciente.id
    )
    telefone = TelefonePacientes(
        tipo=request.form['tipo_telefone'],
        ddd=request.form['ddd'],
        numero=request.form['numero_telefone'],
        id_paciente=novo_paciente.id
    )
    db.session.add(endereco)
    db.session.add(telefone)
    db.session.commit()

    return redirect(url_for('pacientes'))

@app.route('/pacientes/editar/<int:id>', methods=['POST'])
@login_required
def editar_paciente(id):
    paciente = Pacientes.query.get_or_404(id)

    paciente.nome = request.form['nome']
    paciente.cpf = request.form['cpf']
    paciente.sexo = request.form['sexo']
    paciente.email = request.form.get('email')
    paciente.data_nasc = request.form.get('data_nasc')
    paciente.observacoes = request.form.get('observacoes')

    # Atualiza endereço
    if paciente.endereco:
        paciente.endereco.bairro = request.form['bairro']
        paciente.endereco.rua = request.form['rua']
        paciente.endereco.numero = request.form['numero']
        paciente.endereco.cidade = request.form['cidade']
        paciente.endereco.uf = request.form['uf']

    # Atualiza telefone
    if paciente.telefone:
        paciente.telefone.tipo = request.form['tipo_telefone']
        paciente.telefone.ddd = request.form['ddd']
        paciente.telefone.numero = request.form['numero_telefone']

    db.session.commit()
    return redirect(url_for('pacientes'))

@app.route('/pacientes/excluir/<int:id>', methods=['POST'])
@login_required
def excluir_paciente(id):
    paciente = Pacientes.query.get_or_404(id)
    if paciente.endereco:
        db.session.delete(paciente.endereco)
    if paciente.telefone:
        db.session.delete(paciente.telefone)
    db.session.delete(paciente)
    db.session.commit()
    return redirect(url_for('pacientes'))

################################################## FUNCIONARIOS

# Listar funcionários - Apenas ADMIN
@app.route('/funcionarios')
@login_required
def funcionarios():
    if current_user.perfil.nome != 'ADMIN':
        flash('Acesso negado: apenas administradores podem acessar esta área.', 'alert-danger')
        return redirect(url_for('home'))

    funcionarios = Funcionarios.query.all()
    perfis = Perfis.query.all()
    return render_template('funcionarios.html', funcionarios=funcionarios, perfis=perfis)


@app.route('/funcionarios/cadastrar', methods=['POST'])
@login_required
def cadastrar_funcionario():
    if current_user.perfil.nome != 'ADMIN':
        flash('Acesso negado: apenas administradores podem cadastrar funcionários.', 'alert-danger')
        return redirect(url_for('home'))

    nome = request.form['nome']
    cpf = request.form['cpf']
    sexo = request.form['sexo']
    email = request.form['email']
    matricula = request.form['matricula']
    data_nasc = request.form.get('data_nasc')
    senha = request.form['senha']
    id_perfil = request.form['id_perfil']

    senha_hash = generate_password_hash(senha)

    novo_funcionario = Funcionarios(
        nome=nome,
        cpf=cpf,
        sexo=sexo,
        email=email,
        matricula=matricula,
        data_nasc=data_nasc,
        senha_hash=senha_hash,
        id_perfil=id_perfil
    )
    db.session.add(novo_funcionario)
    db.session.commit()

    endereco = EnderecoFuncionarios(
        bairro=request.form['bairro'],
        rua=request.form['rua'],
        numero=request.form['numero'],
        cidade=request.form['cidade'],
        uf=request.form['uf'],
        id_funcionario=novo_funcionario.id_funcionario
    )

    telefone = TelefoneFuncionarios(
        tipo=request.form['tipo_telefone'],
        ddd=request.form['ddd'],
        numero=request.form['numero_telefone'],
        id_funcionario=novo_funcionario.id_funcionario
    )

    db.session.add(endereco)
    db.session.add(telefone)
    db.session.commit()

    flash('Funcionário cadastrado com sucesso.', 'alert-success')
    return redirect(url_for('funcionarios'))


@app.route('/funcionarios/editar/<int:id>', methods=['POST'])
@login_required
def editar_funcionario(id):
    if current_user.perfil.nome != 'ADMIN':
        flash('Acesso negado: apenas administradores podem editar funcionários.', 'alert-danger')
        return redirect(url_for('home'))

    funcionario = Funcionarios.query.get_or_404(id)

    funcionario.nome = request.form['nome']
    funcionario.cpf = request.form['cpf']
    funcionario.sexo = request.form['sexo']
    funcionario.email = request.form['email']
    funcionario.matricula = request.form['matricula']
    funcionario.data_nasc = request.form.get('data_nasc')
    funcionario.id_perfil = int(request.form.get('id_perfil', funcionario.id_perfil))

    nova_senha = request.form.get('senha')
    if nova_senha:
        funcionario.senha_hash = generate_password_hash(nova_senha)

    if funcionario.endereco:
        funcionario.endereco.rua = request.form['rua']
        funcionario.endereco.numero = request.form['numero']
        funcionario.endereco.bairro = request.form['bairro']
        funcionario.endereco.cidade = request.form['cidade']
        funcionario.endereco.uf = request.form['uf']

    if funcionario.telefone:
        funcionario.telefone.tipo = request.form['tipo_telefone']
        funcionario.telefone.ddd = request.form['ddd']
        funcionario.telefone.numero = request.form['numero_telefone']

    db.session.commit()
    flash('Funcionário editado com sucesso.', 'alert-success')
    return redirect(url_for('funcionarios'))


@app.route('/funcionarios/excluir/<int:id>', methods=['POST'])
@login_required
def excluir_funcionario(id):
    if current_user.perfil.nome != 'ADMIN':
        flash('Acesso negado: apenas administradores podem excluir funcionários.', 'alert-danger')
        return redirect(url_for('home'))

    funcionario = Funcionarios.query.get_or_404(id)

    if funcionario.endereco:
        db.session.delete(funcionario.endereco)
    if funcionario.telefone:
        db.session.delete(funcionario.telefone)

    db.session.delete(funcionario)
    db.session.commit()

    flash('Funcionário excluído com sucesso.', 'alert-success')
    return redirect(url_for('funcionarios'))

