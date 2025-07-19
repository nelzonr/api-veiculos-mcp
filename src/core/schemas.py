from typing import Optional, List
from pydantic import BaseModel, Field

class VeiculoFilter(BaseModel):
    """Schema para filtros de busca de veículos."""
    marca: Optional[str] = None
    modelo: Optional[str] = None
    ano: Optional[int] = Field(None, ge=1900)
    motorizacao: Optional[str] = None
    combustivel: Optional[str] = None
    cor: Optional[str] = None
    quilometragem: Optional[int] = Field(None, ge=0)
    numero_portas: Optional[int] = Field(None, ge=2, le=5)
    transmissao: Optional[str] = None
    valor: Optional[float] = Field(None, ge=0)

class PaginatedResponse(BaseModel):
    """Schema para resposta paginada."""
    items: List[dict]
    total: int
    page: int
    page_size: int
    total_pages: int