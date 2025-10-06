"""
Módulo para navegação e paginação.

Responsável por navegar entre páginas e detectar botões
de próxima página.
"""

from typing import Optional

from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webdriver import WebDriver
from selenium.webdriver.remote.webelement import WebElement

from .logger import get_logger

logger = get_logger(__name__)


def verificar_proxima_pagina(driver: WebDriver) -> Optional[WebElement]:
    """
    Verifica se existe próxima página e retorna o botão.
    
    Args:
        driver: Instância do WebDriver
        
    Returns:
        WebElement do botão de próxima página ou None
        
    Examples:
        >>> botao = verificar_proxima_pagina(driver)
        >>> if botao:
        ...     botao.click()
    """
    try:
        # Verificar se há mensagem de "nenhum resultado"
        if _tem_mensagem_sem_resultado(driver):
            logger.info("Detectada mensagem de 'nenhum resultado'")
            return None
        
        # Verificar se há elementos de imóveis na página
        if not _tem_imoveis_na_pagina(driver):
            logger.info("Nenhum elemento de imóvel encontrado na página")
            return None
        
        # Procurar botões de navegação
        botao = _encontrar_botao_proximo(driver)
        
        if botao:
            logger.info(f"Botão de próxima página encontrado: '{botao.text}'")
        else:
            logger.info("Nenhum botão de próxima página válido encontrado")
        
        return botao
        
    except Exception as e:
        logger.error(f"Erro ao verificar próxima página: {e}", exc_info=True)
        return None


def _tem_mensagem_sem_resultado(driver: WebDriver) -> bool:
    """
    Verifica se há mensagem de "nenhum resultado".
    
    Args:
        driver: Instância do WebDriver
        
    Returns:
        True se há mensagem de sem resultado
    """
    xpath = (
        "//*[contains(text(), 'Nenhum resultado') or "
        "contains(text(), 'nenhum resultado') or "
        "contains(text(), 'Não foram encontrados')]"
    )
    mensagens = driver.find_elements(By.XPATH, xpath)
    return len(mensagens) > 0


def _tem_imoveis_na_pagina(driver: WebDriver) -> bool:
    """
    Verifica se há elementos de imóveis na página.
    
    Args:
        driver: Instância do WebDriver
        
    Returns:
        True se há elementos de imóveis
    """
    elementos = driver.find_elements(
        By.CSS_SELECTOR, "a[onclick*='detalhe_imovel']"
    )
    return len(elementos) > 0


def _encontrar_botao_proximo(driver: WebDriver) -> Optional[WebElement]:
    """
    Encontra o botão de próxima página.
    
    Tenta múltiplas estratégias para encontrar o botão.
    
    Args:
        driver: Instância do WebDriver
        
    Returns:
        WebElement do botão ou None
    """
    # Estratégia 1: Botões com texto "Próxima"
    botoes_texto = driver.find_elements(
        By.XPATH,
        "//a[contains(text(), 'Próxima') or "
        "contains(text(), 'Próximo') or "
        "contains(text(), '>') or "
        "contains(text(), 'Seguinte')]"
    )
    
    # Estratégia 2: Botões com href/onclick de paginação
    botoes_href = driver.find_elements(
        By.XPATH,
        "//a[contains(@href, 'pagina') or "
        "contains(@onclick, 'pagina') or "
        "contains(@onclick, 'proxima')]"
    )
    
    # Estratégia 3: Botões com classes específicas
    botoes_classe = driver.find_elements(
        By.CSS_SELECTOR,
        ".proxima, .next, .btn-proximo, .btn-next, "
        "[class*='proxima'], [class*='next']"
    )
    
    # Combinar todas as estratégias
    todos_botoes = botoes_texto + botoes_href + botoes_classe
    
    # Validar botões
    for botao in todos_botoes:
        if _botao_e_valido(botao):
            return botao
    
    # Estratégia 4: Botões numéricos
    return _encontrar_botao_numerico(driver)


def _botao_e_valido(botao: WebElement) -> bool:
    """
    Verifica se um botão é válido para navegação.
    
    Args:
        botao: WebElement do botão
        
    Returns:
        True se o botão é válido
    """
    try:
        if not (botao.is_displayed() and botao.is_enabled()):
            return False
        
        href = botao.get_attribute('href') or ''
        if href == '#':
            return False
        
        classes = (botao.get_attribute('class') or '').lower()
        if 'disabled' in classes:
            return False
        
        texto_botao = botao.text.strip().lower()
        if texto_botao in ['1', 'atual', 'current']:
            return False
        
        return True
        
    except Exception:
        return False


def _encontrar_botao_numerico(driver: WebDriver) -> Optional[WebElement]:
    """
    Encontra botão de paginação numérica.
    
    Args:
        driver: Instância do WebDriver
        
    Returns:
        WebElement do botão ou None
    """
    paginas = driver.find_elements(
        By.XPATH,
        "//a[contains(@class, 'pagina') or contains(@class, 'page')]"
    )
    
    for pagina in paginas:
        try:
            if not (pagina.is_displayed() and pagina.is_enabled()):
                continue
            
            classes = (pagina.get_attribute('class') or '').lower()
            if 'active' in classes or 'current' in classes:
                continue
            
            numero_pagina = pagina.text.strip()
            if numero_pagina.isdigit():
                logger.info(f"Botão de página numérica encontrado: {numero_pagina}")
                return pagina
                
        except Exception:
            continue
    
    return None

