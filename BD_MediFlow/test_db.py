from MediFlow import app, db
from MediFlow.models import Procedimentos

# Inicia o contexto da aplicação Flask antes da consulta ao banco
with app.app_context():
    try:
        procedimentos = Procedimentos.query.all()
        print(f"Procedimentos encontrados: {len(procedimentos)}")
        for procedimento in procedimentos:
            print(f"ID: {procedimento.id}, Nome: {procedimento.nome}, Categoria: {procedimento.categoria}, Preco: {procedimento.preco}, Descricao: {procedimento.descricao}, Ativo: {procedimento.ativo}, Tempo_Estimado: {procedimento.tempo_estimado} ")
    except Exception as e:
        print(f"Erro ao conectar ao banco: {e}")