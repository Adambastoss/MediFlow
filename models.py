from MediFlow import db

class Procedimentos(db.Model):
    __tablename__ = 'PROCEDIMENTOS'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    nome = db.Column(db.String(100), nullable=False)
    categoria = db.Column(db.Enum('CONSULTA', 'EXAME LABORATORIAL', 'EXAME DE IMAGEM', 'VACINA'), nullable=False)
    preco = db.Column(db.Numeric(10, 2), nullable=False)
    descricao = db.Column(db.Text)
    ativo = db.Column(db.Boolean, default=True)
    tempo_estimado = db.Column(db.String(8))