import os
import pytest
import uvicorn
import threading
from dotenv import load_dotenv
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from src.core.database import Base
from src.api.server import app

load_dotenv()

SERVER_HOST = os.getenv("SERVER_HOST_TEST")
SERVER_PORT = os.getenv("SERVER_PORT_TEST")

@pytest.fixture(scope="session")
def db_engine():
    """Configura um banco de dados em memória para testes"""
    engine = create_engine("sqlite:///:memory:")
    
    # Cria todas as tabelas antes dos testes
    Base.metadata.create_all(engine)
    yield engine
    # Limpeza após os testes
    engine.dispose()

@pytest.fixture
def db_session(db_engine):
    """Cria uma sessão limpa para cada teste"""
    connection = db_engine.connect()
    transaction = connection.begin()
    Session = sessionmaker(bind=connection)
    session = Session()
    try:
        yield session
    finally:
        session.close()
        transaction.rollback()
        connection.close()


@pytest.fixture(scope="session")
def test_server():
    # Configuração do servidor de teste
    def run_server():
        uvicorn.run(app, host=SERVER_HOST, port=SERVER_PORT)

    thread = threading.Thread(target=run_server, daemon=True)
    thread.start()
    yield
    # O servidor será encerrado quando os testes terminarem

@pytest.fixture
def client(db_session):
    # Sobrescreve a dependência get_db para usar a sessão de teste
    from fastapi.testclient import TestClient
    from src.api.server import app, get_db
    def override_get_db():
        try:
            yield db_session
        finally:
            pass
    app.dependency_overrides[get_db] = override_get_db
    client = TestClient(app)
    yield client