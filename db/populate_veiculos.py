from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from models import Base, Veiculo
from faker import Faker
import random

engine = create_engine('sqlite:///db/veiculos.db')
Session = sessionmaker(bind=engine)
session = Session()

Base.metadata.create_all(engine)
session.query(Veiculo).delete()
session.commit()

fake = Faker('pt_BR')

quantidade_veiculos = 100
print(f"Populando {quantidade_veiculos} veículos...")

marcas_modelos = [
    ("Fiat", ["Strada", "Argo", "Mobi", "Cronos"]),
    ("Volkswagen", ["Gol", "Polo", "T-Cross", "Saveiro"]),
    ("Chevrolet", ["Onix", "Tracker", "S10", "Cruze"]),
    ("Ford", ["Fiesta", "Ka", "EcoSport", "Ranger"]),
    ("Honda", ["Civic", "HR-V", "Fit", "City"]),
    ("Toyota", ["Corolla", "Hilux", "SW4", "Yaris"]),
    ("Nissan", ["Kicks", "Versa", "Sentra", "Frontier"]),
    ("Hyundai", ["HB20", "Creta", "Tucson", "Santa Fe"]),
    ("Renault", ["Sandero", "Duster", "Captur", "Kwid"]),
    ("Peugeot", ["208", "3008", "2008", "Partner"]),
    ("Citroën", ["C3", "C4 Cactus", "Aircross", "Jumper"])
]
ano_minimo, ano_maximo = 2000, 2025
motorizacoes = ('1.0', '1.3', '1.6', '2.0', '2.4', '3.0')
combustiveis = ('Gasolina', 'Álcool', 'Flex', 'Diesel')
cores = ("Preto", "Branco", "Prata", "Vermelho", "Azul", "Verde", "Amarelo", "Cinza")
km_minimo, km_maximo = 1000, 200000
numero_portas = (2, 4)
transmissoes = ('Manual', 'Automático')
valor_minimo, valor_maximo = 10000, 100000

for _ in range(quantidade_veiculos):
    marca, modelos = random.choice(marcas_modelos)
    veiculo = Veiculo(
        marca=marca,
        modelo=random.choice(modelos),
        ano=fake.random_int(min=ano_minimo, max=ano_maximo),
        motorizacao=fake.random_element(elements=motorizacoes),
        combustivel=fake.random_element(elements=combustiveis),
        cor=fake.random_element(elements=cores),
        quilometragem=fake.random_int(min=km_minimo, max=km_maximo),
        numero_portas=fake.random_element(elements=numero_portas),
        transmissao=fake.random_element(elements=transmissoes),
        valor=fake.random_int(min=valor_minimo, max=valor_maximo),
    )
    session.add(veiculo)

session.commit()
print("Dados de veículos populados com sucesso!")