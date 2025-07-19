from src.core import models

def test_model_veiculo(db_session):
    """Testa a criação de um veiculo"""
    veiculo = models.Veiculo(
        marca="Toyota",
        modelo="Corolla",
        ano=2020,
        motorizacao="2.0",
        combustivel="Gasolina",
        cor="Preto",
        quilometragem=15000,
        numero_portas=4,
        transmissao="Automático",
        valor=90000.00
    )
    db_session.add(veiculo)
    db_session.commit()
    
    # Verifica se foi criado corretamente
    veiculo_no_db = db_session.query(models.Veiculo).first()
    
    assert veiculo_no_db is not None
    assert veiculo_no_db.marca == veiculo.marca
    assert veiculo_no_db.ano == veiculo.ano
    assert veiculo_no_db.motorizacao == veiculo.motorizacao
    assert veiculo_no_db.combustivel == veiculo.combustivel
    assert veiculo_no_db.cor == veiculo.cor
    assert veiculo_no_db.quilometragem == veiculo.quilometragem
    assert veiculo_no_db.numero_portas == veiculo.numero_portas
    assert veiculo_no_db.transmissao == veiculo.transmissao
    assert veiculo_no_db.valor == veiculo.valor
    assert veiculo_no_db.id is not None
    assert veiculo_no_db.id > 0