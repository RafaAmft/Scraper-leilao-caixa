"""
Sistema de logging centralizado.

Implementa logging profissional seguindo boas práticas,
substituindo prints por logging estruturado.
"""

import logging
import sys
from pathlib import Path
from typing import Optional
from datetime import datetime

from .config import LOGS_DIR


class _SemDuplicarNoConsole(logging.Filter):
    """Silencia o console deste logger quando o logger raiz já escreve no console.

    O ``scraper_automatico.py`` configura o logger raiz (``config/logging_config``)
    e as mensagens dos módulos propagam até ele; sem este filtro, cada linha
    aparecia duas vezes no terminal. Usado sozinho (sem logger raiz configurado),
    o módulo continua escrevendo no console normalmente.
    """

    def filter(self, record: logging.LogRecord) -> bool:
        raiz = logging.getLogger()
        return not any(
            type(h) is logging.StreamHandler and getattr(h, "stream", None) in (sys.stdout, sys.stderr)
            for h in raiz.handlers
        )


def setup_logger(
    name: str = "scraper",
    level: int = logging.INFO,
    log_to_file: bool = True,
    log_to_console: bool = True,
) -> logging.Logger:
    """
    Configura e retorna um logger.
    
    Args:
        name: Nome do logger
        level: Nível de log (DEBUG, INFO, WARNING, ERROR, CRITICAL)
        log_to_file: Se deve salvar logs em arquivo
        log_to_console: Se deve exibir logs no console
        
    Returns:
        Logger configurado
        
    Examples:
        >>> logger = setup_logger("meu_modulo")
        >>> logger.info("Operação iniciada")
        >>> logger.error("Erro encontrado", exc_info=True)
    """
    # Criar logger
    logger = logging.getLogger(name)
    logger.setLevel(level)
    
    # Evitar handlers duplicados
    if logger.handlers:
        return logger
    
    # Formato detalhado
    formatter = logging.Formatter(
        fmt="%(asctime)s | %(levelname)-8s | %(name)s | %(funcName)s:%(lineno)d | %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S",
    )
    
    # Handler para console
    if log_to_console:
        console_handler = logging.StreamHandler(sys.stdout)
        console_handler.setLevel(level)
        console_handler.setFormatter(formatter)
        console_handler.addFilter(_SemDuplicarNoConsole())
        logger.addHandler(console_handler)
    
    # Handler para arquivo
    if log_to_file:
        timestamp = datetime.now().strftime("%Y%m%d")
        log_file = LOGS_DIR / f"{name}_{timestamp}.log"
        
        file_handler = logging.FileHandler(log_file, encoding="utf-8")
        file_handler.setLevel(level)
        file_handler.setFormatter(formatter)
        logger.addHandler(file_handler)
    
    return logger


# Logger global padrão
logger = setup_logger()


def get_logger(name: Optional[str] = None) -> logging.Logger:
    """
    Retorna um logger configurado.
    
    Args:
        name: Nome do logger. Se None, retorna o logger global.
        
    Returns:
        Logger configurado
    """
    if name is None:
        return logger
    return setup_logger(name)

