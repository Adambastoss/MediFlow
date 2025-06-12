<<<<<<< HEAD
from flask import Flask, render_template, url_for, flash, redirect, request, session
from MediFlow import app, db
from MediFlow.forms import FormLogin
from MediFlow.models import Procedimentos, Pacientes, EnderecoPacientes, TelefonePacientes, Funcionarios, EnderecoFuncionarios, TelefoneFuncionarios, Perfis
from werkzeug.security import generate_password_hash, check_password_hash
from functools import wraps
from flask_login import login_required, current_user, login_user, logout_user
=======
from flask import Flask, render_template, url_for, flash, redirect, request
from MediFlow import app, db # Importa a instância do app e do db
from MediFlow.forms import FormLogin
# --- MUDANÇA AQUI: Importa o módulo models em vez de classes individuais ---
from MediFlow import models 
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import login_user, logout_user, login_required, current_user 
>>>>>>> 36e070927fd26816203fceb0352bf48ab2070dc8

@app.route('/', methods=['GET', 'POST'])
def login():
    # Se o usuário já estiver logado, redireciona para a página inicial
    if current_user.is_authenticated:
        return redirect(url_for('home'))

    form_login = FormLogin()
    if form_login.validate_on_submit():
<<<<<<< HEAD
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
=======
        cpf_digitado = form_login.cpf.data

        # Opcional: Limpar o CPF se o banco de dados armazena apenas números
        # Ex: "123.456.789-00" -> "12345678900"
        cpf_limpo = ''.join(filter(str.isdigit, cpf_digitado))

        # Busca o funcionário pelo CPF
        # --- MUDANÇA AQUI: Usa models.Funcionarios ---
        funcionario = models.Funcionarios.query.filter_by(cpf=cpf_limpo).first()

        # Verifica se o funcionário existe e se a senha está correta
        if funcionario and check_password_hash(funcionario.senha_hash, senha_digitada):
            login_user(funcionario, remember=form_login.lembrar_dados.data) # Loga o usuário
            flash(f'Login realizado com sucesso para {funcionario.nome}!', 'alert-success')
            
            # Redireciona para a página que o usuário tentou acessar antes do login, se houver
            next_page = request.args.get('next')
            return redirect(next_page or url_for('home'))
        else:
            flash('Falha no login. Verifique seu CPF e senha.', 'alert-danger')
    return render_template('login.html', form_login=form_login)




@app.route('/logout')
@login_required # Garante que só usuários logados podem fazer logout
def logout():
    logout_user() # Desloga o usuário
    flash('Sessão encerrada com sucesso!', 'alert-info')
    return redirect(url_for('login'))


@app.route('/home')
@login_required # Protege esta rota, exigindo login para acesso
>>>>>>> 36e070927fd26816203fceb0352bf48ab2070dc8
def home():
    return render_template('home.html')


@app.route('/consultas')
<<<<<<< HEAD
@login_required
=======
@login_required # Protege esta rota
>>>>>>> 36e070927fd26816203fceb0352bf48ab2070dc8
def consultas():
    # Acesso: Admin, Médico
    # --- MUDANÇA AQUI: Usa current_user.perfil.nome ---
    if current_user.perfil.nome not in ['Admin', 'Médico']:
        flash('Você não tem permissão para acessar Consultas.', 'alert-danger')
        return redirect(url_for('home')) # Redireciona para a home ou uma página de erro
    return render_template('consultas.html')


################################################## PROCEDIMENTOS 
@app.route('/procedimentos')
<<<<<<< HEAD
@login_required
=======
@login_required # Protege esta rota
>>>>>>> 36e070927fd26816203fceb0352bf48ab2070dc8
def procedimentos():
    # Acesso: Admin, Recepcionista
    if current_user.perfil.nome not in ['Admin', 'Recepcionista']:
        flash('Você não tem permissão para gerenciar Procedimentos.', 'alert-danger')
        return redirect(url_for('home'))
    # --- MUDANÇA AQUI: Usa models.Procedimentos ---
    procedimentos = models.Procedimentos.query.all()
    return render_template('procedimentos.html', procedimentos=procedimentos)

@app.route('/procedimentos/editar/<int:id>', methods=['POST'])
<<<<<<< HEAD
@login_required
=======
@login_required # Protege esta rota
>>>>>>> 36e070927fd26816203fceb0352bf48ab2070dc8
def editar_procedimento_modal(id):
    if current_user.perfil.nome not in ['Admin', 'Recepcionista']:
        flash('Você não tem permissão para editar Procedimentos.', 'alert-danger')
        return redirect(url_for('procedimentos'))
    # --- MUDANÇA AQUI: Usa models.Procedimentos ---
    procedimento = models.Procedimentos.query.get_or_404(id)

    procedimento.nome = request.form['nome']
    procedimento.categoria = request.form['categoria']
    procedimento.preco = request.form['preco']
    procedimento.descricao = request.form['descricao']
    procedimento.ativo = True if request.form.get('ativo') == 'on' else False
    procedimento.tempo_estimado = request.form['tempo_estimado']

    db.session.commit()
    flash('Procedimento editado com sucesso!', 'alert-success')
    return redirect(url_for('procedimentos'))

@app.route('/procedimentos/excluir/<int:id>', methods=['POST'])
<<<<<<< HEAD
@login_required
=======
@login_required # Protege esta rota
>>>>>>> 36e070927fd26816203fceb0352bf48ab2070dc8
def excluir_procedimento(id):
    if current_user.perfil.nome not in ['Admin', 'Recepcionista']:
        flash('Você não tem permissão para excluir Procedimentos.', 'alert-danger')
        return redirect(url_for('procedimentos'))
    # --- MUDANÇA AQUI: Usa models.Procedimentos ---
    procedimento = models.Procedimentos.query.get_or_404(id)
    db.session.delete(procedimento)
    db.session.commit()
    flash('Procedimento excluído com sucesso!', 'alert-success')
    return redirect(url_for('procedimentos'))

@app.route('/procedimentos/cadastrar', methods=['POST'])
<<<<<<< HEAD
@login_required
=======
@login_required # Protege esta rota
>>>>>>> 36e070927fd26816203fceb0352bf48ab2070dc8
def cadastrar_procedimento():
    if current_user.perfil.nome not in ['Admin', 'Recepcionista']:
        flash('Você não tem permissão para cadastrar Procedimentos.', 'alert-danger')
        return redirect(url_for('procedimentos'))
    nome = request.form['nome']
    categoria = request.form['categoria']
    preco = request.form['preco']
    descricao = request.form['descricao']
    ativo = True if request.form.get('ativo') == 'on' else False
    tempo_estimado = request.form['tempo_estimado']

    # --- MUDANÇA AQUI: Usa models.Procedimentos ---
    novo_procedimento = models.Procedimentos(
        nome=nome,
        categoria=categoria,
        preco=preco,
        descricao=descricao,
        ativo=ativo,
        tempo_estimado=tempo_estimado
    )

    db.session.add(novo_procedimento)
    db.session.commit()
    flash('Procedimento cadastrado com sucesso!', 'alert-success')
    return redirect(url_for('procedimentos'))

################################################## PACIENTES
@app.route('/pacientes')
<<<<<<< HEAD
@login_required
=======
@login_required # Protege esta rota
>>>>>>> 36e070927fd26816203fceb0352bf48ab2070dc8
def pacientes():
    # Acesso: Admin, Recepcionista, Médico
    if current_user.perfil.nome not in ['Admin', 'Recepcionista', 'Médico']:
        flash('Você não tem permissão para gerenciar Pacientes.', 'alert-danger')
        return redirect(url_for('home'))
    # --- MUDANÇA AQUI: Usa models.Pacientes ---
    pacientes = models.Pacientes.query.all()
    return render_template('pacientes.html', pacientes=pacientes)

@app.route('/pacientes/cadastrar', methods=['POST'])
<<<<<<< HEAD
@login_required
=======
@login_required # Protege esta rota
>>>>>>> 36e070927fd26816203fceb0352bf48ab2070dc8
def cadastrar_paciente():
    if current_user.perfil.nome not in ['Admin', 'Recepcionista']: # Médicos não podem cadastrar/excluir por padrão
        flash('Você não tem permissão para cadastrar Pacientes.', 'alert-danger')
        return redirect(url_for('pacientes'))
    nome = request.form['nome']
    cpf = request.form['cpf']
    sexo = request.form['sexo']
    email = request.form.get('email')
    data_nasc = request.form.get('data_nasc')
    observacoes = request.form.get('observacoes')

    # --- MUDANÇA AQUI: Usa models.Pacientes ---
    novo_paciente = models.Pacientes(
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
    # --- MUDANÇA AQUI: Usa models.EnderecoPacientes e models.TelefonePacientes ---
    endereco = models.EnderecoPacientes(
        bairro=request.form['bairro'],
        rua=request.form['rua'],
        numero=request.form['numero'],
        cidade=request.form['cidade'],
        uf=request.form['uf'],
        id_paciente=novo_paciente.id
    )
    telefone = models.TelefonePacientes(
        tipo=request.form['tipo_telefone'],
        ddd=request.form['ddd'],
        numero=request.form['numero_telefone'],
        id_paciente=novo_paciente.id
    )
    db.session.add(endereco)
    db.session.add(telefone)
    db.session.commit()
    flash('Paciente cadastrado com sucesso!', 'alert-success')
    return redirect(url_for('pacientes'))

@app.route('/pacientes/editar/<int:id>', methods=['POST'])
<<<<<<< HEAD
@login_required
=======
@login_required # Protege esta rota
>>>>>>> 36e070927fd26816203fceb0352bf48ab2070dc8
def editar_paciente(id):
    if current_user.perfil.nome not in ['Admin', 'Recepcionista']: # Médicos não podem cadastrar/excluir por padrão
        flash('Você não tem permissão para editar Pacientes.', 'alert-danger')
        return redirect(url_for('pacientes'))
    # --- MUDANÇA AQUI: Usa models.Pacientes ---
    paciente = models.Pacientes.query.get_or_404(id)

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
    else: # Cria se não existir (garantia, caso os campos não fossem obrigatórios no HTML)
        # --- MUDANÇA AQUI: Usa models.EnderecoPacientes ---
        endereco = models.EnderecoPacientes(
            bairro=request.form['bairro'],
            rua=request.form['rua'],
            numero=request.form['numero'],
            cidade=request.form['cidade'],
            uf=request.form['uf'],
            id_paciente=paciente.id
        )
        db.session.add(endereco)


    # Atualiza telefone
    if paciente.telefone:
        paciente.telefone.tipo = request.form['tipo_telefone']
        paciente.telefone.ddd = request.form['ddd']
        paciente.telefone.numero = request.form['numero_telefone']
    else: # Cria se não existir (garantia)
        # --- MUDANÇA AQUI: Usa models.TelefonePacientes ---
        telefone = models.TelefonePacientes(
            tipo=request.form['tipo_telefone'],
            ddd=request.form['ddd'],
            numero=request.form['numero_telefone'],
            id_paciente=paciente.id
        )
        db.session.add(telefone)


    db.session.commit()
    flash('Paciente editado com sucesso!', 'alert-success')
    return redirect(url_for('pacientes'))

@app.route('/pacientes/excluir/<int:id>', methods=['POST'])
<<<<<<< HEAD
@login_required
=======
@login_required # Protege esta rota
>>>>>>> 36e070927fd26816203fceb0352bf48ab2070dc8
def excluir_paciente(id):
    if current_user.perfil.nome not in ['Admin', 'Recepcionista']: # Médicos não podem cadastrar/excluir por padrão
        flash('Você não tem permissão para excluir Pacientes.', 'alert-danger')
        return redirect(url_for('pacientes'))
    # --- MUDANÇA AQUI: Usa models.Pacientes ---
    paciente = models.Pacientes.query.get_or_404(id)
    if paciente.endereco:
        db.session.delete(paciente.endereco)
    if paciente.telefone:
        db.session.delete(paciente.telefone)
    db.session.delete(paciente)
    db.session.commit()
    flash('Paciente excluído com sucesso!', 'alert-success')
    return redirect(url_for('pacientes'))

################################################## FUNCIONARIOS

# Listar funcionários - Apenas ADMIN
@app.route('/funcionarios')
<<<<<<< HEAD
@login_required
def funcionarios():
    if current_user.perfil.nome != 'ADMIN':
        flash('Acesso negado: apenas administradores podem acessar esta área.', 'alert-danger')
        return redirect(url_for('home'))

    funcionarios = Funcionarios.query.all()
    perfis = Perfis.query.all()
=======
@login_required # Protege esta rota
def funcionarios():
    # Acesso: Apenas Admin pode gerenciar outros funcionários
    if current_user.perfil.nome != 'Admin':
        flash('Você não tem permissão para gerenciar Funcionários.', 'alert-danger')
        return redirect(url_for('home')) # Redireciona para a home
    # --- MUDANÇA AQUI: Usa models.Funcionarios e models.Perfis ---
    funcionarios = models.Funcionarios.query.all()
    perfis = models.Perfis.query.all()
>>>>>>> 36e070927fd26816203fceb0352bf48ab2070dc8
    return render_template('funcionarios.html', funcionarios=funcionarios, perfis=perfis)


@app.route('/funcionarios/cadastrar', methods=['POST'])
<<<<<<< HEAD
@login_required
def cadastrar_funcionario():
    if current_user.perfil.nome != 'ADMIN':
        flash('Acesso negado: apenas administradores podem cadastrar funcionários.', 'alert-danger')
        return redirect(url_for('home'))

=======
@login_required # Protege esta rota
def cadastrar_funcionario():
    if current_user.perfil.nome != 'Admin':
        flash('Você não tem permissão para cadastrar Funcionários.', 'alert-danger')
        return redirect(url_for('funcionarios'))
>>>>>>> 36e070927fd26816203fceb0352bf48ab2070dc8
    nome = request.form['nome']
    cpf = request.form['cpf']
    sexo = request.form['sexo']
    email = request.form['email']
    matricula = request.form['matricula']
    data_nasc = request.form.get('data_nasc')
<<<<<<< HEAD
    senha = request.form['senha']
    id_perfil = request.form['id_perfil']

    senha_hash = generate_password_hash(senha)

    novo_funcionario = Funcionarios(
=======
    
    senha = request.form['senha']
    confirmar_senha = request.form['confirmar_senha']

    if senha != confirmar_senha:
        flash('A senha e a confirmação de senha não coincidem!', 'alert-danger')
        return redirect(url_for('funcionarios'))

    senha_hash = generate_password_hash(senha)
    id_perfil = request.form['id_perfil']

    # --- MUDANÇA AQUI: Usa models.Funcionarios ---
    novo_funcionario = models.Funcionarios(
>>>>>>> 36e070927fd26816203fceb0352bf48ab2070dc8
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

<<<<<<< HEAD
    endereco = EnderecoFuncionarios(
=======
    # Endereço
    # --- MUDANÇA AQUI: Usa models.EnderecoFuncionarios e models.TelefoneFuncionarios ---
    endereco = models.EnderecoFuncionarios(
>>>>>>> 36e070927fd26816203fceb0352bf48ab2070dc8
        bairro=request.form['bairro'],
        rua=request.form['rua'],
        numero=request.form['numero'],
        cidade=request.form['cidade'],
        uf=request.form['uf'],
        id_funcionario=novo_funcionario.id_funcionario
    )
<<<<<<< HEAD

    telefone = TelefoneFuncionarios(
=======
    # Telefone
    telefone = models.TelefoneFuncionarios(
>>>>>>> 36e070927fd26816203fceb0352bf48ab2070dc8
        tipo=request.form['tipo_telefone'],
        ddd=request.form['ddd'],
        numero=request.form['numero_telefone'],
        id_funcionario=novo_funcionario.id_funcionario
    )

    db.session.add(endereco)
    db.session.add(telefone)
    db.session.commit()
<<<<<<< HEAD

    flash('Funcionário cadastrado com sucesso.', 'alert-success')
=======
    flash('Funcionário cadastrado com sucesso!', 'alert-success')
>>>>>>> 36e070927fd26816203fceb0352bf48ab2070dc8
    return redirect(url_for('funcionarios'))


@app.route('/funcionarios/editar/<int:id>', methods=['POST'])
<<<<<<< HEAD
@login_required
def editar_funcionario(id):
    if current_user.perfil.nome != 'ADMIN':
        flash('Acesso negado: apenas administradores podem editar funcionários.', 'alert-danger')
        return redirect(url_for('home'))

    funcionario = Funcionarios.query.get_or_404(id)
=======
@login_required # Protege esta rota
def editar_funcionario(id):
    if current_user.perfil.nome != 'Admin':
        flash('Você não tem permissão para editar Funcionários.', 'alert-danger')
        return redirect(url_for('funcionarios'))
    # --- MUDANÇA AQUI: Usa models.Funcionarios ---
    funcionario = models.Funcionarios.query.get_or_404(id)
>>>>>>> 36e070927fd26816203fceb0352bf48ab2070dc8

    funcionario.nome = request.form['nome']
    funcionario.cpf = request.form['cpf']
    funcionario.sexo = request.form['sexo']
    funcionario.email = request.form['email']
    funcionario.matricula = request.form['matricula']
    funcionario.data_nasc = request.form.get('data_nasc')
<<<<<<< HEAD
    funcionario.id_perfil = int(request.form.get('id_perfil', funcionario.id_perfil))

    nova_senha = request.form.get('senha')
    if nova_senha:
        funcionario.senha_hash = generate_password_hash(nova_senha)
=======
    funcionario.id_perfil = request.form['id_perfil']

    nova_senha = request.form.get('senha')
    confirmar_nova_senha = request.form.get('confirmar_senha')

    if nova_senha: # Se uma nova senha foi fornecida
        if nova_senha != confirmar_nova_senha:
            flash('A nova senha e a confirmação de senha não coincidem!', 'alert-danger')
            return redirect(url_for('funcionarios'))
        senha_hash = generate_password_hash(nova_senha) # Gera o hash da nova senha
        funcionario.senha_hash = senha_hash # Atualiza o hash da senha do funcionário
>>>>>>> 36e070927fd26816203fceb0352bf48ab2070dc8

    if funcionario.endereco:
        funcionario.endereco.rua = request.form['rua']
        funcionario.endereco.numero = request.form['numero']
        funcionario.endereco.bairro = request.form['bairro']
        funcionario.endereco.cidade = request.form['cidade']
        funcionario.endereco.uf = request.form['uf']
    else: # Criar endereço se não existir (garantia)
        # --- MUDANÇA AQUI: Usa models.EnderecoFuncionarios ---
        endereco = models.EnderecoFuncionarios(
            bairro=request.form['bairro'],
            rua=request.form['rua'],
            numero=request.form['numero'],
            cidade=request.form['cidade'],
            uf=request.form['uf'],
            id_funcionario=funcionario.id_funcionario
        )
        db.session.add(endereco)

    if funcionario.telefone:
        funcionario.telefone.tipo = request.form['tipo_telefone']
        funcionario.telefone.ddd = request.form['ddd']
        funcionario.telefone.numero = request.form['numero_telefone']
    else: # Criar telefone se não existir (garantia)
        # --- MUDANÇA AQUI: Usa models.TelefoneFuncionarios ---
        telefone = models.TelefoneFuncionarios(
            tipo=request.form['tipo_telefone'],
            ddd=request.form['ddd'],
            numero=request.form['numero_telefone'],
            id_funcionario=funcionario.id_funcionario
        )
        db.session.add(telefone)

    db.session.commit()
<<<<<<< HEAD
    flash('Funcionário editado com sucesso.', 'alert-success')
=======
    flash('Funcionário atualizado com sucesso!', 'alert-success')
>>>>>>> 36e070927fd26816203fceb0352bf48ab2070dc8
    return redirect(url_for('funcionarios'))


@app.route('/funcionarios/excluir/<int:id>', methods=['POST'])
<<<<<<< HEAD
@login_required
def excluir_funcionario(id):
    if current_user.perfil.nome != 'ADMIN':
        flash('Acesso negado: apenas administradores podem excluir funcionários.', 'alert-danger')
        return redirect(url_for('home'))

    funcionario = Funcionarios.query.get_or_404(id)

=======
@login_required # Protege esta rota
def excluir_funcionario(id):
    if current_user.perfil.nome != 'Admin':
        flash('Você não tem permissão para excluir Funcionários.', 'alert-danger')
        return redirect(url_for('funcionarios'))
    # --- MUDANÇA AQUI: Usa models.Funcionarios ---
    funcionario = models.Funcionarios.query.get_or_404(id)
>>>>>>> 36e070927fd26816203fceb0352bf48ab2070dc8
    if funcionario.endereco:
        db.session.delete(funcionario.endereco)
    if funcionario.telefone:
        db.session.delete(funcionario.telefone)

    db.session.delete(funcionario)
    db.session.commit()
<<<<<<< HEAD

    flash('Funcionário excluído com sucesso.', 'alert-success')
    return redirect(url_for('funcionarios'))

=======
    flash('Funcionário excluído com sucesso!', 'alert-success')
    return redirect(url_for('funcionarios'))
>>>>>>> 36e070927fd26816203fceb0352bf48ab2070dc8
