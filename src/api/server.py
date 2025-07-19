import os
from dotenv import load_dotenv
from typing import Optional
from fastapi import FastAPI, Depends, HTTPException, Query
from fastapi_mcp import FastApiMCP
from sqlalchemy import desc
from sqlalchemy.orm import Session
from sqlalchemy.exc import SQLAlchemyError
from core.logger import logger
from core.database import get_db
from core.models import Veiculo
from core.schemas import PaginatedResponse

load_dotenv()

SERVER_HOST = os.getenv("SERVER_HOST")
SERVER_PORT = int(os.getenv("SERVER_PORT"))
PAGINATION_LIMIT = int(os.getenv("PAGINATION_LIMIT", 10))

# Aplicação FastAPI
app = FastAPI(
    title="API de Veículos",
    description="API para busca e gerenciamento de veículos",
    version="1.0.0"
)

@app.get(
    "/",
    operation_id="buscar_veiculos",
    response_model=PaginatedResponse,
    summary="Buscar veículos",
    description="Retorna uma lista paginada de veículos com base nos filtros fornecidos"
)
def buscar_veiculos(
    marca: Optional[str] = None,
    modelo: Optional[str] = None,
    ano: Optional[int] = None,
    motorizacao: Optional[str] = None,
    combustivel: Optional[str] = None,
    cor: Optional[str] = None,
    quilometragem: Optional[int] = Query(None, ge=0),
    numero_portas: Optional[int] = Query(None, ge=2, le=5),
    transmissao: Optional[str] = None,
    valor: Optional[float] = Query(None, ge=0),
    ordenar_por: Optional[str] = Query(None, description="Campo para ordenação"),
    ordem: Optional[str] = Query("asc", enum=["asc", "desc"]),
    page: int = Query(1, ge=1, description="Número da página"),
    page_size: int = Query(PAGINATION_LIMIT, ge=1, le=100, description="Itens por página"),
    db: Session = Depends(get_db)
):
    """
    Busca veículos com base nos filtros fornecidos.
    
    Args:
        marca: Marca do veículo
        modelo: Modelo do veículo
        ano: Ano de fabricação
        motorizacao: Motorização do veículo
        combustivel: Tipo de combustível
        cor: Cor do veículo
        quilometragem: Quilometragem do veículo
        numero_portas: Número de portas
        transmissao: Tipo de transmissão
        valor: Valor do veículo
        ordenar_por: Campo para ordenação
        ordem: Ordem da ordenação (asc/desc)
        page: Número da página
        page_size: Itens por página
        
    Returns:
        Lista paginada de veículos que correspondem aos filtros
    """
    try:
        # Construir query base
        query = db.query(Veiculo)

        # Aplicar filtros
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

        # Aplicar ordenação
        if ordenar_por:
            if hasattr(Veiculo, ordenar_por):
                ordem_attr = getattr(Veiculo, ordenar_por)
                if ordem == "desc":
                    query = query.order_by(desc(ordem_attr))
                else:
                    query = query.order_by(ordem_attr)

        # Calcular total e páginas
        total = query.count()
        total_pages = (total + page_size - 1) // page_size

        # Aplicar paginação
        query = query.offset((page - 1) * page_size).limit(page_size)
        veiculos = query.all()

        if not veiculos:
            raise HTTPException(
                status_code=404,
                detail="Nenhum veículo encontrado"
            )

        # Converter veículos para dicionários
        veiculos_dict = [
            {
                "id": v.id,
                "marca": v.marca,
                "modelo": v.modelo,
                "ano": v.ano,
                "motorizacao": v.motorizacao,
                "combustivel": v.combustivel,
                "cor": v.cor,
                "quilometragem": v.quilometragem,
                "numero_portas": v.numero_portas,
                "transmissao": v.transmissao,
                "valor": v.valor
            }
            for v in veiculos
        ]

        return PaginatedResponse(
            items=veiculos_dict,
            total=total,
            page=page,
            page_size=page_size,
            total_pages=total_pages
        )

    except SQLAlchemyError as e:
        logger.error(f"Erro ao buscar veículos: {str(e)}")
        raise HTTPException(
            status_code=500,
            detail="Erro interno ao buscar veículos"
        )

if __name__ == "__main__":
    mcp = FastApiMCP(app, include_operations=["buscar_veiculos"])
    mcp.mount()

    import uvicorn
    uvicorn.run(app, host=SERVER_HOST, port=SERVER_PORT)
