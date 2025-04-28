from flask import Flask, render_template, url_for, flash, redirect, request
from MediFlow import app, db
from MediFlow.forms import FormLogin
from MediFlow.models import Procedimentos, Pacientes, EnderecoPacientes, TelefonePacientes, Funcionarios, EnderecoFuncionarios, TelefoneFuncionarios, Perfis
from werkzeug.security import generate_password_hash


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


@app.route('/consultas')
def consultas():
    return render_template('consultas.html')


################################################## PROCEDIMENTOS   
@app.route('/procedimentos')
def procedimentos():
    procedimentos = Procedimentos.query.all() 
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

################################################## PACIENTES
@app.route('/pacientes')
def pacientes():
    pacientes = Pacientes.query.all()
    return render_template('pacientes.html', pacientes=pacientes)

@app.route('/pacientes/cadastrar', methods=['POST'])
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
@app.route('/funcionarios')
def funcionarios():
    funcionarios = Funcionarios.query.all()
    perfis = Perfis.query.all()  # <-- busca os perfis
    return render_template('funcionarios.html', funcionarios=funcionarios, perfis=perfis)


@app.route('/funcionarios/cadastrar', methods=['POST'])
def cadastrar_funcionario():
    nome = request.form['nome']
    cpf = request.form['cpf']
    sexo = request.form['sexo']
    email = request.form['email']
    matricula = request.form['matricula']
    data_nasc = request.form.get('data_nasc')
    senha_hash = generate_password_hash('123456')  # exemplo, depois a gente pode melhorar isso
    id_perfil = request.form['id_perfil']

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

    # Endereço
    endereco = EnderecoFuncionarios(
        bairro=request.form['bairro'],
        rua=request.form['rua'],
        numero=request.form['numero'],
        cidade=request.form['cidade'],
        uf=request.form['uf'],
        id_funcionario=novo_funcionario.id_funcionario
    )
    # Telefone
    telefone = TelefoneFuncionarios(
        tipo=request.form['tipo_telefone'],
        ddd=request.form['ddd'],
        numero=request.form['numero_telefone'],
        id_funcionario=novo_funcionario.id_funcionario
    )
    db.session.add(endereco)
    db.session.add(telefone)
    db.session.commit()

    return redirect(url_for('funcionarios'))


@app.route('/funcionarios/editar/<int:id>', methods=['POST'])
def editar_funcionario(id):
    funcionario = Funcionarios.query.get_or_404(id)

    funcionario.nome = request.form['nome']
    funcionario.cpf = request.form['cpf']
    funcionario.sexo = request.form['sexo']
    funcionario.email = request.form['email']
    funcionario.matricula = request.form['matricula']
    funcionario.data_nasc = request.form.get('data_nasc')

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
    return redirect(url_for('funcionarios'))

@app.route('/funcionarios/excluir/<int:id>', methods=['POST'])
def excluir_funcionario(id):
    funcionario = Funcionarios.query.get_or_404(id)
    if funcionario.endereco:
        db.session.delete(funcionario.endereco)
    if funcionario.telefone:
        db.session.delete(funcionario.telefone)
    db.session.delete(funcionario)
    db.session.commit()
    return redirect(url_for('funcionarios'))


