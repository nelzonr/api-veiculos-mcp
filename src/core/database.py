import os
from pathlib import Path
from dotenv import load_dotenv
from core.logger import logger
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base

load_dotenv()

DATABASE_PATH = Path(__file__).parent.parent.parent / os.getenv("DATABASE_PATH")
DATABASE_URL = os.getenv("DATABASE_URL", f"sqlite:///{DATABASE_PATH}")

# Criação da engine
try:
    logger.info(f"Conectando ao banco de dados: {DATABASE_URL}")
    engine = create_engine(
        DATABASE_URL,
        connect_args={"check_same_thread": False}  # Necessário para SQLite
    )
except Exception as e:
    logger.error(f"Erro ao criar engine do banco de dados: {e}")
    raise

# Fábrica de sessões
try:
    SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
except Exception as e:
    logger.error(f"Erro ao configurar SessionLocal: {e}")
    raise

# Base para os modelos ORM
Base = declarative_base()

def create_tables():
    """
    Cria as tabelas do banco de dados se não existirem.
    Deve ser chamado uma vez ao iniciar o app ou scripts utilitários.
    """
    try:
        Base.metadata.create_all(engine)
        logger.info("Tabelas criadas/verificadas com sucesso.")
    except Exception as e:
        logger.error(f"Erro ao criar/verificar tabelas: {e}")
        raise

def get_db():
    """
    Fornece uma instância de banco de dados para cada requisição.
    """
    db = SessionLocal()
    logger.info("Sessão de banco de dados iniciada.")
    try:
        yield db
    finally:
        db.close()
        logger.info("Sessão de banco de dados fechada.")