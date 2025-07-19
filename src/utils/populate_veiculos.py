import random
from faker import Faker
from sqlalchemy.exc import SQLAlchemyError
from core.logger import logger
from core.database import create_tables, SessionLocal
from core.models import Veiculo

# Inicializar Faker com localização brasileira
fake = Faker("pt_BR")

# Configurações para geração dos veiculos
QUANTIDADE_VEICULOS = 100
MARCAS_MODELOS = [
    ("Fiat", ["Strada", "Argo", "Mobi", "Cronos"]),
    ("Volkswagen", ["Gol", "Polo", "T-Cross", "Saveiro"]),
    ("Chevrolet", ["Onix", "Tracker", "S10", "Cruze"]),
    ("Ford", ["Fiesta", "Ka", "EcoSport", "Ranger"]),
    ("Honda", ["Civic", "HR-V", "Fit", "City"]),
    ("Toyota", ["Corolla", "Hilux", "SW4", "Yaris"]),
    ("Nissan", ["Kicks", "Versa", "Sentra", "Frontier"]),
    ("Hyundai", ["HB20", "Creta", "Tucson", "Santa Fe"]),
    ("Renault", ["Sandero", "Duster", "Captur", "Kwid"]),
    ("Peugeot", ["208", "3008", "2008", "Partner"])
]
ANO_MINIMO, ANO_MAXIMO = 2000, 2025
MOTORIZACOES = ('1.0', '1.3', '1.6', '2.0', '2.4', '3.0')
COMBUSTIVEIS = ('Gasolina', 'Álcool', 'Flex', 'Diesel')
CORES = ("Preto", "Branco", "Prata", "Vermelho", "Azul", "Verde", "Amarelo", "Cinza")
KM_MINIMO, KM_MAXIMO = 1000, 200000
NUMERO_PORTAS = (2, 4)
TRANSMISSOES = ('Manual', 'Automático')
VALOR_MINIMO, VALOR_MAXIMO = 10000, 100000

def populate_veiculos():
    """Popula o banco de dados com veículos fictícios."""

    create_tables()
    session = SessionLocal()

    # Limpar tabela antes de popular
    try:
        session.query(Veiculo).delete()
        session.commit()
        logger.info("Tabela de veículos limpa antes da população.")
    except SQLAlchemyError as e:
        logger.error(f"Erro ao limpar tabela de veículos: {str(e)}")
        session.rollback()
        session.close()
        return False

    veiculos_adicionados = 0
    try:
        logger.info(f"Iniciando população de {QUANTIDADE_VEICULOS} veículos...")

        for _ in range(QUANTIDADE_VEICULOS):
            try:
                marca, modelos = random.choice(MARCAS_MODELOS)
                veiculo = Veiculo(
                    marca=marca,
                    modelo=random.choice(modelos),
                    ano=fake.random_int(min=ANO_MINIMO, max=ANO_MAXIMO),
                    motorizacao=fake.random_element(elements=MOTORIZACOES),
                    combustivel=fake.random_element(elements=COMBUSTIVEIS),
                    cor=fake.random_element(elements=CORES),
                    quilometragem=fake.random_int(min=KM_MINIMO, max=KM_MAXIMO),
                    numero_portas=fake.random_element(elements=NUMERO_PORTAS),
                    transmissao=fake.random_element(elements=TRANSMISSOES),
                    valor=fake.random_int(min=VALOR_MINIMO, max=VALOR_MAXIMO),
                )
                session.add(veiculo)
                veiculos_adicionados += 1
                
                # Commit a cada 10 veículos para evitar transações muito grandes
                if veiculos_adicionados % 10 == 0:
                    session.commit()
                    logger.info(f"Adicionados {veiculos_adicionados} veículos...")
                
            except SQLAlchemyError as e:
                logger.error(f"Erro ao adicionar veículo: {str(e)}")
                session.rollback()
                continue

        # Commit final para garantir que todos os veículos foram salvos
        session.commit()
        logger.info(f"População concluída com sucesso! {veiculos_adicionados} veículos adicionados.")
        return True
        
    except SQLAlchemyError as e:
        logger.error(f"Erro na conexão com o banco de dados: {str(e)}")
        if session:
            session.rollback()
        return False
    
    finally:
        if session:
            session.close()
        logger.info("Sessão de banco de dados fechada.")


def main():
    """Função principal do script."""
    if populate_veiculos():
        logger.info("Script executado com sucesso!")
    else:
        logger.error("Falha ao popular veículos.")

if __name__ == "__main__":
    main()