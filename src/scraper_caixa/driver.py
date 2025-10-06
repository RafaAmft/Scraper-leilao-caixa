"""
Módulo para configuração e gerenciamento do ChromeDriver.

Responsável por configurar o Selenium WebDriver com opções
anti-detecção e gerenciamento robusto de erros.
"""

import os
from typing import Optional

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.remote.webdriver import WebDriver
from webdriver_manager.chrome import ChromeDriverManager

from .config import (
    CHROME_OPTIONS,
    CHROME_EXPERIMENTAL_OPTIONS,
    USER_AGENT,
    ScraperConfig,
)
from .exceptions import ChromeDriverError
from .logger import get_logger

logger = get_logger(__name__)


def configurar_chrome_options(headless: bool = True) -> Options:
    """
    Configura as opções do Chrome.
    
    Args:
        headless: Se deve executar em modo headless (sem interface gráfica)
        
    Returns:
        Objeto Options configurado
        
    Examples:
        >>> options = configurar_chrome_options(headless=True)
        >>> options.headless
        True
    """
    chrome_options = Options()
    
    # Adicionar opções básicas
    for option in CHROME_OPTIONS:
        chrome_options.add_argument(option)
    
    # Adicionar user agent
    chrome_options.add_argument(f"--user-agent={USER_AGENT}")
    
    # Modo headless
    if headless:
        chrome_options.add_argument("--headless")
        logger.info("Modo headless ativado")
    
    # Opções experimentais
    for key, value in CHROME_EXPERIMENTAL_OPTIONS.items():
        chrome_options.add_experimental_option(key, value)
    
    return chrome_options


def remover_indicadores_automacao(driver: WebDriver) -> None:
    """
    Remove indicadores de automação do navegador.
    
    Args:
        driver: Instância do WebDriver
        
    Raises:
        ChromeDriverError: Se falhar ao executar o script
    """
    try:
        driver.execute_script(
            "Object.defineProperty(navigator, 'webdriver', {get: () => undefined})"
        )
        logger.debug("Indicadores de automação removidos")
    except Exception as e:
        logger.warning(f"Falha ao remover indicadores de automação: {e}")


def configurar_chromedriver(
    config: Optional[ScraperConfig] = None
) -> WebDriver:
    """
    Configura e retorna uma instância do ChromeDriver.
    
    Tenta configurar o ChromeDriver usando múltiplas estratégias:
    1. ChromeDriverManager (recomendado)
    2. ChromeDriver do sistema
    3. Caminho manual para sistemas Unix
    
    Args:
        config: Configuração do scraper. Se None, usa configuração padrão.
        
    Returns:
        Instância configurada do WebDriver
        
    Raises:
        ChromeDriverError: Se todas as tentativas falharem
        
    Examples:
        >>> driver = configurar_chromedriver()
        >>> driver.get("https://www.google.com")
        >>> driver.quit()
    """
    if config is None:
        config = ScraperConfig()
    
    logger.info("Iniciando configuração do ChromeDriver...")
    
    chrome_options = configurar_chrome_options(headless=config.headless)
    
    # Tentativa 1: ChromeDriverManager
    try:
        logger.info("Tentando ChromeDriverManager...")
        driver_path = ChromeDriverManager().install()
        
        if not os.path.isfile(driver_path):
            raise ChromeDriverError(f"ChromeDriver não encontrado em: {driver_path}")
        
        logger.info(f"ChromeDriver encontrado em: {driver_path}")
        
        service = Service(driver_path)
        driver = webdriver.Chrome(service=service, options=chrome_options)
        
        remover_indicadores_automacao(driver)
        
        logger.info("✅ ChromeDriver configurado via ChromeDriverManager")
        return driver
        
    except Exception as e:
        logger.warning(f"ChromeDriverManager falhou: {e}")
    
    # Tentativa 2: ChromeDriver do sistema
    try:
        logger.info("Tentando ChromeDriver do sistema...")
        driver = webdriver.Chrome(options=chrome_options)
        
        remover_indicadores_automacao(driver)
        
        logger.info("✅ ChromeDriver configurado via sistema")
        return driver
        
    except Exception as e:
        logger.warning(f"ChromeDriver do sistema falhou: {e}")
    
    # Tentativa 3: Caminho manual (Unix)
    try:
        logger.info("Tentando caminho manual Unix...")
        service = Service("/usr/bin/chromedriver")
        driver = webdriver.Chrome(service=service, options=chrome_options)
        
        remover_indicadores_automacao(driver)
        
        logger.info("✅ ChromeDriver configurado via caminho manual")
        return driver
        
    except Exception as e:
        logger.error(f"Caminho manual falhou: {e}")
    
    # Todas as tentativas falharam
    error_msg = (
        "Não foi possível configurar o ChromeDriver. "
        "Certifique-se de que o Chrome está instalado."
    )
    logger.error(error_msg)
    raise ChromeDriverError(error_msg)

