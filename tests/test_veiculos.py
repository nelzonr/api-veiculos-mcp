import os
from dotenv import load_dotenv
import requests
from jsonschema import validate

load_dotenv()

URL_BASE = os.getenv("URL_BASE") + "/veiculos"

schema_resposta = {
    "type": "object",
    "properties": {
        "id": {"type": "number"},
        "marca": {"type": "string"},
        "modelo": {"type": "string"},
        "ano": {"type": "number"},
        "motorizacao": {"type": "string"},
        "combustivel": {"type": "string"},
        "cor": {"type": "string"},
        "quilometragem": {"type": "number"},
        "numero_portas": {"type": "number"},
        "transmissao": {"type": "string"},
        "valor": {"type": "number"}
    },
    "required": ["id", "marca", "modelo", "ano", "motorizacao", "combustivel", "cor", "quilometragem", "numero_portas", "transmissao", "valor"]
}


def test_listar_veiculos():
    response = requests.get(URL_BASE)
    assert response.status_code == 200
    assert isinstance(response.json(), list)
    assert len(response.json()) > 0

def test_listar_veiculos_fiat():
    response = requests.get(URL_BASE + "/?marca=Fiat")
    assert response.status_code == 200
    validate(instance=response.json()[0], schema=schema_resposta)

def test_veiculo_inexistente():
    response = requests.get(URL_BASE + "/?marca=Ferrari")
    assert response.status_code == 200
    assert response.json()["error"] == "Veiculo não encontrado"

def test_tempo_resposta():
    response = requests.get(URL_BASE)
    assert response.elapsed.total_seconds() < 0.5  # 500ms
