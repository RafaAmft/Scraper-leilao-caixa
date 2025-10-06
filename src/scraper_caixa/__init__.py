"""
Scraper de Imóveis da Caixa Econômica Federal.

Versão 1.1.0 - Refatorado seguindo boas práticas de código.

Este pacote fornece ferramentas para buscar e extrair informações
de imóveis em leilão da Caixa Econômica Federal.
"""

__version__ = "1.1.0"
__author__ = "Rafael Fontes"
__email__ = "rafael.a.fontes@hotmail.com"

# Imports principais
from .config import ScraperConfig, ESTADOS_CIDADES, TIPOS_IMOVEL
from .driver import configurar_chromedriver
from .exceptions import (
    ScraperError,
    ChromeDriverError,
    NavigationError,
    ElementNotFoundError,
    DataExtractionError,
)
from .logger import get_logger, setup_logger
from .types import FiltrosBusca, DadosImovel, ResultadoBusca

__all__ = [
    # Version
    "__version__",
    # Config
    "ScraperConfig",
    "ESTADOS_CIDADES",
    "TIPOS_IMOVEL",
    # Driver
    "configurar_chromedriver",
    # Exceptions
    "ScraperError",
    "ChromeDriverError",
    "NavigationError",
    "ElementNotFoundError",
    "DataExtractionError",
    # Logger
    "get_logger",
    "setup_logger",
    # Types
    "FiltrosBusca",
    "DadosImovel",
    "ResultadoBusca",
]
