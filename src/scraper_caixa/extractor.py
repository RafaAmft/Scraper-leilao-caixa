"""
Módulo para extração de dados de imóveis.

Responsável por extrair informações dos elementos HTML
e transformá-los em dados estruturados.
"""

import re
from typing import Optional, Dict, Any

from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webelement import WebElement

from .logger import get_logger
from .types import DadosImovel

logger = get_logger(__name__)


def extrair_dados_imovel(elemento: WebElement) -> Optional[Dict[str, Any]]:
    """
    Extrai dados de um elemento HTML de imóvel.
    
    Args:
        elemento: Elemento WebElement do Selenium
        
    Returns:
        Dicionário com dados do imóvel ou None se falhar
        
    Examples:
        >>> dados = extrair_dados_imovel(elemento)
        >>> if dados:
        ...     print(dados['nome_imovel'])
    """
    try:
        # Procurar pelo link com os dados do imóvel
        link_element = elemento.find_element(
            By.CSS_SELECTOR, "a[onclick*='detalhe_imovel']"
        )
        texto_completo = link_element.text.strip()
        
        # Extrair informações usando regex
        # Padrão: "CIDADE - NOME DO IMÓVEL | R$ VALOR"
        match = re.search(r'([^-]+) - (.+?) \| R\$ (.+)', texto_completo)
        
        if not match:
            logger.warning(f"Padrão não encontrado no texto: {texto_completo}")
            return None
        
        cidade = match.group(1).strip()
        nome_imovel = match.group(2).strip()
        valor = match.group(3).strip()
        
        # Extrair ID do imóvel do onclick
        onclick = link_element.get_attribute('onclick')
        id_match = re.search(r'detalhe_imovel\((\d+)\)', onclick)
        id_imovel = id_match.group(1) if id_match else ''
        
        # Gerar link direto para o imóvel
        link_direto = (
            f"https://venda-imoveis.caixa.gov.br/sistema/"
            f"detalhe-imovel.asp?hdnOrigem=index&txtImovel={id_imovel}"
            if id_imovel else ''
        )
        
        # Extrair URL da imagem
        url_imagem = _extrair_url_imagem(elemento)
        
        # Extrair informações adicionais
        endereco, quartos = _extrair_informacoes_adicionais(elemento)
        
        return {
            'id_imovel': id_imovel,
            'cidade': cidade,
            'nome_imovel': nome_imovel,
            'valor': valor,
            'endereco': endereco,
            'quartos': quartos,
            'url_imagem': url_imagem,
            'link_direto': link_direto,
            'texto_completo': texto_completo
        }
        
    except Exception as e:
        logger.error(f"Erro ao extrair dados do imóvel: {e}", exc_info=True)
        return None


def _extrair_url_imagem(elemento: WebElement) -> str:
    """
    Extrai URL da imagem do imóvel.
    
    Args:
        elemento: Elemento WebElement do Selenium
        
    Returns:
        URL da imagem ou string vazia
    """
    try:
        img_element = elemento.find_element(By.CSS_SELECTOR, "img.fotoimovel")
        return img_element.get_attribute('src') or ''
    except Exception:
        return ''


def _extrair_informacoes_adicionais(elemento: WebElement) -> tuple[str, str]:
    """
    Extrai informações adicionais do imóvel (endereço e quartos).
    
    Args:
        elemento: Elemento WebElement do Selenium
        
    Returns:
        Tupla (endereco, quartos)
    """
    endereco = ''
    quartos = ''
    
    try:
        texto_elemento = elemento.text
        
        # Padrões para extrair endereço
        endereco_patterns = [
            r'Endereço[:\s]+([^\n]+)',
            r'Localização[:\s]+([^\n]+)',
            r'Bairro[:\s]+([^\n]+)',
            r'Rua[:\s]+([^\n]+)',
            r'Av[:\s]+([^\n]+)'
        ]
        
        for pattern in endereco_patterns:
            endereco_match = re.search(pattern, texto_elemento, re.IGNORECASE)
            if endereco_match:
                endereco = endereco_match.group(1).strip()
                break
        
        # Padrões para extrair quartos
        quartos_patterns = [
            r'(\d+)\s*quarto',
            r'(\d+)\s*suíte',
            r'(\d+)\s*dormitório',
            r'(\d+)\s*bedroom'
        ]
        
        for pattern in quartos_patterns:
            quartos_match = re.search(pattern, texto_elemento, re.IGNORECASE)
            if quartos_match:
                quartos = quartos_match.group(1)
                break
                
    except Exception as e:
        logger.debug(f"Erro ao extrair informações adicionais: {e}")
    
    return endereco, quartos


def extrair_imoveis_via_regex(html_source: str) -> list[Dict[str, Any]]:
    """
    Extrai imóveis diretamente do HTML usando regex.
    
    Método de fallback quando os seletores CSS não funcionam.
    
    Args:
        html_source: Código HTML da página
        
    Returns:
        Lista de dicionários com dados dos imóveis
        
    Examples:
        >>> imoveis = extrair_imoveis_via_regex(html)
        >>> len(imoveis)
        5
    """
    logger.info("Usando extração via regex como fallback")
    
    padrao_imoveis = r'([^-]+) - ([^|]+) \| R\$ ([^<]+)'
    matches = re.findall(padrao_imoveis, html_source)
    
    imoveis = []
    for i, match in enumerate(matches, 1):
        cidade = match[0].strip()
        nome_imovel = match[1].strip()
        valor = match[2].strip()
        
        imovel = {
            'numero': i,
            'cidade': cidade,
            'nome_imovel': nome_imovel,
            'valor': valor,
            'id_imovel': '',
            'url_imagem': '',
            'endereco': '',
            'quartos': '',
            'link_direto': '',
            'texto_completo': f"{cidade} - {nome_imovel} | R$ {valor}",
        }
        imoveis.append(imovel)
        logger.debug(f"Imóvel {i}: {nome_imovel} - R$ {valor}")
    
    return imoveis

