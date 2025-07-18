from fastapi import FastAPI, Depends
from sqlalchemy.orm import Session
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from db.models import Base, Veiculo

DATABASE_URL = "sqlite:///db/veiculos.db"

engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base.metadata.create_all(bind=engine)

app = FastAPI()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.get("/veiculos")
def buscar_veiculos(
    marca: str = None,
    modelo: str = None,
    ano: int = None,
    motorizacao: str = None,
    combustivel: str = None,
    cor: str = None,
    quilometragem: int = None,
    numero_portas: int = None,
    transmissao: str = None,
    valor: float = None,
    db: Session = Depends(get_db)
):
    query = db.query(Veiculo)
    if marca: query = query.filter(Veiculo.marca == marca)
    if modelo: query = query.filter(Veiculo.modelo == modelo)
    if ano: query = query.filter(Veiculo.ano == ano)
    if motorizacao: query = query.filter(Veiculo.motorizacao == motorizacao)
    if combustivel: query = query.filter(Veiculo.combustivel == combustivel)
    if cor: query = query.filter(Veiculo.cor == cor)
    if quilometragem: query = query.filter(Veiculo.quilometragem == quilometragem)
    if numero_portas: query = query.filter(Veiculo.numero_portas == numero_portas)
    if transmissao: query = query.filter(Veiculo.transmissao == transmissao)
    if valor: query = query.filter(Veiculo.valor == valor)
    return query.all()