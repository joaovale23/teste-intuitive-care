from sqlalchemy import (
    Column, Integer, String, Numeric, Date, CHAR
)
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()


class DespesaConsolidada(Base):
    __tablename__ = "despesas_consolidadas"

    id = Column(Integer, primary_key=True, autoincrement=True)
    cnpj = Column(String(20))
    razao_social = Column(String(255))
    registro_ans = Column(String(20))
    trimestre = Column(Integer, nullable=False)
    ano = Column(Integer, nullable=False)
    valor_despesas = Column(Numeric(18, 2), nullable=False)


class Operadora(Base):
    __tablename__ = "operadoras"

    registro_ans = Column(String(20), primary_key=True)
    cnpj = Column(String(20), nullable=False)
    razao_social = Column(String(255), nullable=False)
    nome_fantasia = Column(String(255))
    modalidade = Column(String(100))
    logradouro = Column(String(255))
    numero = Column(String(20))
    complemento = Column(String(255))
    bairro = Column(String(100))
    cidade = Column(String(100))
    uf = Column(CHAR(2))
    cep = Column(String(10))
    ddd = Column(String(5))
    telefone = Column(String(20))
    fax = Column(String(20))
    endereco_eletronico = Column(String(255))
    representante = Column(String(255))
    cargo_representante = Column(String(255))
    regiao_comercializacao = Column(String(100))
    data_registro_ans = Column(Date)


class DespesaAgregada(Base):
    __tablename__ = "despesas_agregadas"

    id = Column(Integer, primary_key=True, autoincrement=True)
    cnpj = Column(String(20), nullable=False)
    razao_social = Column(String(255), nullable=False)
    registro_ans = Column(String(20), nullable=False)
    modalidade = Column(String(100))
    uf = Column(CHAR(2), nullable=False)
    trimestre = Column(Integer, nullable=False)
    ano = Column(Integer, nullable=False)
    valor_despesas = Column(Numeric(18, 2), nullable=False)
    media_trimestral = Column(Numeric(18, 2))
    desvio_padrao = Column(Numeric(18, 2))
