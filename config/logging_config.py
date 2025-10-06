#!/usr/bin/env python3
"""
Configuração de logging estruturado para o Scraper Imóveis Caixa
"""

import logging
import os
from datetime import datetime
from logging.handlers import RotatingFileHandler

def setup_logging(log_level=logging.INFO, log_to_file=True, log_to_console=True):
    """
    Configura o sistema de logging estruturado
    
    Args:
        log_level: Nível de log (DEBUG, INFO, WARNING, ERROR, CRITICAL)
        log_to_file: Se deve salvar logs em arquivo
        log_to_console: Se deve mostrar logs no console
    """
    
    # Criar diretório de logs
    logs_dir = 'logs'
    os.makedirs(logs_dir, exist_ok=True)
    
    # Nome do arquivo de log com timestamp
    timestamp = datetime.now().strftime("%Y%m%d")
    log_filename = os.path.join(logs_dir, f'scraper_{timestamp}.log')
    
    # Configurar formato do log
    log_format = '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    date_format = '%Y-%m-%d %H:%M:%S'
    
    # Configurar logger raiz
    root_logger = logging.getLogger()
    root_logger.setLevel(log_level)
    
    # Limpar handlers existentes para evitar duplicação
    for handler in root_logger.handlers[:]:
        root_logger.removeHandler(handler)
    
    # Handler para arquivo com rotação
    if log_to_file:
        file_handler = RotatingFileHandler(
            log_filename,
            maxBytes=10*1024*1024,  # 10MB
            backupCount=5,
            encoding='utf-8'
        )
        file_handler.setLevel(log_level)
        file_formatter = logging.Formatter(log_format, date_format)
        file_handler.setFormatter(file_formatter)
        root_logger.addHandler(file_handler)
    
    # Handler para console
    if log_to_console:
        console_handler = logging.StreamHandler()
        console_handler.setLevel(log_level)
        console_formatter = logging.Formatter(log_format, date_format)
        console_handler.setFormatter(console_formatter)
        root_logger.addHandler(console_handler)
    
    # Logger específico para o scraper
    scraper_logger = logging.getLogger('scraper_caixa')
    scraper_logger.setLevel(log_level)
    
    # Log de inicialização
    scraper_logger.info("=" * 60)
    scraper_logger.info("🚀 SISTEMA DE LOGS INICIALIZADO")
    scraper_logger.info(f"📅 Data/Hora: {datetime.now().strftime('%d/%m/%Y %H:%M:%S')}")
    scraper_logger.info(f"📁 Arquivo de log: {log_filename}")
    scraper_logger.info(f"🔧 Nível de log: {logging.getLevelName(log_level)}")
    scraper_logger.info("=" * 60)
    
    return scraper_logger

def get_logger(name='scraper_caixa'):
    """
    Retorna um logger configurado
    
    Args:
        name: Nome do logger
        
    Returns:
        Logger configurado
    """
    return logging.getLogger(name)

def log_performance(func):
    """
    Decorator para logar performance de funções
    
    Args:
        func: Função a ser decorada
        
    Returns:
        Função decorada com logging de performance
    """
    import time
    import functools
    
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        logger = get_logger('performance')
        start_time = time.time()
        
        try:
            result = func(*args, **kwargs)
            end_time = time.time()
            execution_time = end_time - start_time
            
            logger.info(f"⏱️ {func.__name__} executada em {execution_time:.2f}s")
            return result
            
        except Exception as e:
            end_time = time.time()
            execution_time = end_time - start_time
            
            logger.error(f"❌ {func.__name__} falhou após {execution_time:.2f}s: {e}")
            raise
    
    return wrapper

def log_errors(func):
    """
    Decorator para logar erros de funções
    
    Args:
        func: Função a ser decorada
        
    Returns:
        Função decorada com logging de erros
    """
    import functools
    
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        logger = get_logger('errors')
        
        try:
            return func(*args, **kwargs)
            
        except Exception as e:
            logger.error(f"❌ Erro em {func.__name__}: {e}", exc_info=True)
            raise
    
    return wrapper

# Configuração padrão
if __name__ == "__main__":
    # Teste da configuração
    logger = setup_logging(log_level=logging.DEBUG)
    logger.info("✅ Sistema de logs testado com sucesso!")
    logger.debug("🔍 Modo debug ativado")
    logger.warning("⚠️ Aviso de teste")
    logger.error("❌ Erro de teste")

