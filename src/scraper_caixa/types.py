"""
Definições de tipos para type hints.

Centraliza as definições de tipos customizados usados no projeto.
"""

from typing import Dict, List, Optional, TypedDict
from dataclasses import dataclass


class FiltrosBusca(TypedDict, total=False):
    """Tipos para filtros de busca de imóveis."""
    
    estado: str
    codigo_cidade: str
    nome_cidade: str
    tipo_imovel: Optional[str]
    faixa_valor: Optional[str]
    quartos: Optional[str]


class DadosImovel(TypedDict, total=False):
    """Tipos para dados de um imóvel."""
    
    id_imovel: str
    nome_imovel: str
    endereco: str
    cidade: str
    estado: str
    valor: str
    quartos: Optional[str]
    link_direto: Optional[str]
    pagina: int
    data_extracao: str


@dataclass
class ResultadoBusca:
    """Resultado de uma busca de imóveis."""
    
    imoveis: List[DadosImovel]
    total: int
    cidade: str
    estado: str
    timestamp: str
    sucesso: bool
    erro: Optional[str] = None

