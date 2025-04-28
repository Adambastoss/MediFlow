from MediFlow import db

class Procedimentos(db.Model):
    __tablename__ = 'PROCEDIMENTOS'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    nome = db.Column(db.String(100), nullable=False)
    categoria = db.Column(db.Enum('CONSULTA', 'EXAME LABORATORIAL', 'EXAME DE IMAGEM', 'VACINA'), nullable=False)
    preco = db.Column(db.Numeric(10, 2), nullable=False)
    descricao = db.Column(db.Text)
    ativo = db.Column(db.Boolean, default=True)
    tempo_estimado = db.Column(db.Integer)

class Pacientes(db.Model):
    __tablename__ = 'PACIENTES'
    
    id = db.Column('ID_PACIENTE', db.Integer, primary_key=True, autoincrement=True)
    nome = db.Column('NOME', db.String(100), nullable=False)
    cpf = db.Column('CPF', db.String(16), nullable=False)
    sexo = db.Column('SEXO', db.Enum('M', 'F'), nullable=False)
    email = db.Column('EMAIL', db.String(50), unique=True)
    data_nasc = db.Column('DATA_NASC', db.Date)
    observacoes = db.Column('OBSERVACOES', db.Text)

    endereco = db.relationship('EnderecoPacientes', uselist=False, backref='paciente')
    telefone = db.relationship('TelefonePacientes', uselist=False, backref='paciente')

class EnderecoPacientes(db.Model):
    __tablename__ = 'ENDERECO_PACIENTES'

    id = db.Column('ID_ENDERECO', db.Integer, primary_key=True, autoincrement=True)
    bairro = db.Column('BAIRRO', db.String(60), nullable=False)
    rua = db.Column('RUA', db.String(60), nullable=False)
    numero = db.Column('NUMERO', db.Integer, nullable=False)
    cidade = db.Column('CIDADE', db.String(40), nullable=False)
    uf = db.Column('UF', db.String(2), nullable=False)
    id_paciente = db.Column('ID_PACIENTE', db.Integer, db.ForeignKey('PACIENTES.ID_PACIENTE'), unique=True)

class TelefonePacientes(db.Model):
    __tablename__ = 'TELEFONE_PACIENTES'

    id = db.Column('ID_TELEFONE', db.Integer, primary_key=True, autoincrement=True)
    tipo = db.Column('TIPO', db.Enum('RES', 'COM', 'CEL'), nullable=False)
    ddd = db.Column('DDD', db.String(5), nullable=False)
    numero = db.Column('NUMERO', db.String(15), nullable=False)
    id_paciente = db.Column('ID_PACIENTE', db.Integer, db.ForeignKey('PACIENTES.ID_PACIENTE'), unique=True)
    


class Perfis(db.Model):
    __tablename__ = 'perfis'
    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(50), nullable=False)



class Funcionarios(db.Model):
    __tablename__ = 'funcionarios'
    id_funcionario = db.Column(db.Integer, primary_key=True, autoincrement=True)
    nome = db.Column(db.String(100), nullable=False)
    cpf = db.Column(db.String(16), unique=True, nullable=False)
    data_nasc = db.Column(db.Date)
    sexo = db.Column(db.Enum('M', 'F'), nullable=False)
    email = db.Column(db.String(100), unique=True, nullable=False)
    matricula = db.Column(db.String(20), unique=True, nullable=False)
    senha_hash = db.Column(db.String(255), nullable=False)
    id_perfil = db.Column(db.Integer, db.ForeignKey('perfis.id'), nullable=False)

    perfil = db.relationship('Perfis', backref='funcionarios', lazy=True)
    endereco = db.relationship('EnderecoFuncionarios', backref='funcionario', uselist=False)
    telefone = db.relationship('TelefoneFuncionarios', backref='funcionario', uselist=False)

class EnderecoFuncionarios(db.Model):
    __tablename__ = 'endereco_funcionarios'
    id_endereco = db.Column(db.Integer, primary_key=True, autoincrement=True)
    bairro = db.Column(db.String(60), nullable=False)
    rua = db.Column(db.String(60), nullable=False)
    numero = db.Column(db.Integer, nullable=False)
    cidade = db.Column(db.String(40), nullable=False)
    uf = db.Column(db.String(2), nullable=False)
    id_funcionario = db.Column(db.Integer, db.ForeignKey('funcionarios.id_funcionario'), unique=True)

class TelefoneFuncionarios(db.Model):
    __tablename__ = 'telefone_funcionarios'
    id_telefone = db.Column(db.Integer, primary_key=True, autoincrement=True)
    tipo = db.Column(db.Enum('RES', 'COM', 'CEL'), nullable=False)
    ddd = db.Column(db.String(5), nullable=False)
    numero = db.Column(db.String(15), nullable=False)
    id_funcionario = db.Column(db.Integer, db.ForeignKey('funcionarios.id_funcionario'))
