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
from .csv_loader import (
    CAIXA_CSV_URL,
    baixar_csv_caixa,
    buscar_imoveis_csv,
    carregar_csv_caixa,
    filtrar_imoveis_csv,
    obter_csv_caixa,
    carregar_ou_baixar_csv,
    filtrar_cidades_configuradas,
)
from .painel import gerar_painel_html
from .gmail_oauth import enviar_email_oauth, obter_servico_gmail
try:
    from .driver import configurar_chromedriver
except ImportError:
    configurar_chromedriver = None  # type: ignore[assignment]
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
    # CSV Loader
    "CAIXA_CSV_URL",
    "baixar_csv_caixa",
    "carregar_csv_caixa",
    "filtrar_imoveis_csv",
    "buscar_imoveis_csv",
    "obter_csv_caixa",
    "carregar_ou_baixar_csv",
    "filtrar_cidades_configuradas",
    # Painel
    "gerar_painel_html",
    # Gmail OAuth2
    "obter_servico_gmail",
    "enviar_email_oauth",
]
