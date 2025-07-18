from sqlalchemy import Column, Integer, Float, String
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class Veiculo(Base):
    __tablename__ = "veiculos"
    
    id = Column(Integer, primary_key=True)
    marca = Column(String, nullable=False)
    modelo = Column(String, nullable=False)
    ano = Column(Integer, nullable=False)
    motorizacao = Column(String, nullable=False)
    combustivel = Column(String, nullable=False)
    cor = Column(String, nullable=False)
    quilometragem = Column(Integer, nullable=False)
    numero_portas = Column(Integer, nullable=False)
    transmissao = Column(String, nullable=False)
    valor = Column(Float, nullable=False)

    def __repr__(self):
        return f"<Veiculo(id={self.id}, marca={self.marca}, modelo='{self.modelo}', ano={self.ano}, cor='{self.cor}')>, valor={self.valor}>"
    
    def __init__(self, marca, modelo, ano, motorizacao, combustivel, cor, quilometragem, numero_portas, transmissao, valor):
        self.marca = marca
        self.modelo = modelo
        self.ano = ano
        self.motorizacao = motorizacao
        self.combustivel = combustivel
        self.cor = cor
        self.quilometragem = quilometragem
        self.numero_portas = numero_portas
        self.transmissao = transmissao
        self.valor = valor
