"""
Configurações centralizadas do scraper.

Este módulo contém todas as configurações do projeto,
seguindo as boas práticas de separar configs de código.
"""

from dataclasses import dataclass, field
from typing import Dict, List, Optional
from pathlib import Path

# URLs e constantes
URL_BASE = "https://venda-imoveis.caixa.gov.br/sistema/busca-imovel.asp?sltTipoBusca=imoveis"

# Configurações do Chrome
CHROME_OPTIONS = [
    "--window-size=1920,1080",
    "--no-sandbox",
    "--disable-dev-shm-usage",
    "--disable-gpu",
    "--disable-blink-features=AutomationControlled",
    "--disable-extensions",
    "--disable-plugins",
    "--disable-images",
    "--disable-web-security",
    "--allow-running-insecure-content",
    "--disable-features=VizDisplayCompositor",
    "--disable-ipc-flooding-protection",
]

CHROME_EXPERIMENTAL_OPTIONS = {
    "excludeSwitches": ["enable-automation"],
    "useAutomationExtension": False,
}

USER_AGENT = (
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
    "(KHTML, like Gecko) Chrome/139.0.0.0 Safari/537.36"
)

# Timeouts e tentativas
DEFAULT_TIMEOUT = 30  # segundos
MAX_RETRIES = 3
RETRY_DELAY = 2  # segundos
PAGE_LOAD_DELAY = 3  # segundos

# Diretórios
BASE_DIR = Path(__file__).parent.parent.parent
DATA_DIR = BASE_DIR / "dados_imoveis"
SCREENSHOTS_DIR = BASE_DIR / "screenshots"
REPORTS_DIR = BASE_DIR / "relatorios"
LOGS_DIR = BASE_DIR / "logs"

# Criar diretórios se não existirem
for directory in [DATA_DIR, SCREENSHOTS_DIR, REPORTS_DIR, LOGS_DIR]:
    directory.mkdir(parents=True, exist_ok=True)


@dataclass
class ScraperConfig:
    """Configuração do scraper."""
    
    headless: bool = True
    timeout: int = DEFAULT_TIMEOUT
    max_retries: int = MAX_RETRIES
    retry_delay: int = RETRY_DELAY
    page_load_delay: int = PAGE_LOAD_DELAY
    save_screenshots: bool = True
    save_json: bool = True
    save_csv: bool = True
    
    # Diretórios de saída
    data_dir: Path = field(default_factory=lambda: DATA_DIR)
    screenshots_dir: Path = field(default_factory=lambda: SCREENSHOTS_DIR)
    reports_dir: Path = field(default_factory=lambda: REPORTS_DIR)
    

# Dicionário de estados e cidades
ESTADOS_CIDADES: Dict[str, Dict[str, str]] = {
    "SC": {
        "8690": "JOINVILLE",
        "8621": "FLORIANOPOLIS",
        "8545": "BLUMENAU",
        "8558": "BRUSQUE",
        "8598": "CRICIUMA",
        "8564": "CAMBORIU",
        "8687": "JARAGUA DO SUL",
        "8500": "BARRA VELHA",
        "8510": "BALNEARIO PICARRAS",
        "8520": "ITAJAI",
        "8530": "GOVERNADOR CELSO RAMOS",
    },
    "SP": {
        "3550308": "SAO PAULO",
        "3509502": "CAMPINAS",
        "3548708": "SANTOS",
        "3543402": "RIBEIRAO PRETO",
        "3506607": "BARUERI",
        "3548500": "SANTO ANDRE",
    },
    "RS": {
        "4314902": "PORTO ALEGRE",
        "4304606": "CAXIAS DO SUL",
        "4316907": "SANTA MARIA",
        "4320000": "PELOTAS",
        "4307005": "GRAVATAI",
    },
    "PR": {
        "4106902": "CURITIBA",
        "4113700": "LONDRINA",
        "4104808": "CASCAVEL",
        "4115200": "MARINGA",
        "4101804": "APUCARANA",
    },
    "MG": {
        "3106200": "BELO HORIZONTE",
        "3170206": "UBERLANDIA",
        "3149309": "POUSO ALEGRE",
        "3136702": "JUIZ DE FORA",
    },
    "RJ": {
        "3304557": "RIO DE JANEIRO",
        "3303500": "NOVA IGUACU",
        "3301702": "DUQUE DE CAXIAS",
        "3303302": "NITEROI",
    },
    "BA": {
        "2927408": "SALVADOR",
        "2910800": "FEIRA DE SANTANA",
        "2921005": "ILHEUS",
        "2929206": "VITORIA DA CONQUISTA",
    },
    "CE": {
        "2304400": "FORTALEZA",
        "2303709": "CAUCAIA",
        "2307650": "JUAZEIRO DO NORTE",
        "2312908": "SOBRAL",
    },
    "PE": {
        "2611606": "RECIFE",
        "2609600": "JABOATAO DOS GUARARAPES",
        "2607901": "PETROPOLIS",
    },
    "GO": {
        "5208707": "GOIANIA",
        "5201405": "ANAPOLIS",
        "5218806": "RIO VERDE",
        "5201108": "AGUAS LINDAS DE GOIAS",
    },
    "MT": {
        "5103403": "CUIABA",
        "5102504": "CACERES",
        "5107602": "RONDONOPOLIS",
    },
    "MS": {
        "5002704": "CAMPO GRANDE",
        "5003207": "CORUMBA",
        "5004106": "DOURADOS",
    },
}

# Tipos de imóveis
TIPOS_IMOVEL: Dict[str, str] = {
    "1": "Casa",
    "2": "Apartamento",
    "4": "Indiferente",
}

# Faixas de valor
FAIXAS_VALOR: Dict[str, str] = {
    "1": "Até R$ 50.000",
    "2": "R$ 50.000 a R$ 100.000",
    "3": "R$ 100.000 a R$ 150.000",
    "4": "R$ 150.000 a R$ 200.000",
    "5": "R$ 200.000 a R$ 300.000",
    "6": "R$ 300.000 a R$ 500.000",
    "7": "Acima de R$ 500.000",
}

# Quartos
QUARTOS_OPCOES: Dict[str, str] = {
    "1": "1 quarto",
    "2": "2 quartos",
    "3": "3 quartos",
    "4": "4+ quartos",
}

