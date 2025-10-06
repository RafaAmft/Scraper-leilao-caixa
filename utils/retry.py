#!/usr/bin/env python3
"""
Sistema de retry automático para o Scraper Imóveis Caixa
"""

import time
import random
from functools import wraps
from typing import Callable, Any, Optional, Union
from config.logging_config import get_logger

logger = get_logger('retry')

class RetryConfig:
    """Configuração para retry automático"""
    
    def __init__(self, 
                 max_attempts: int = 3,
                 base_delay: float = 1.0,
                 max_delay: float = 60.0,
                 exponential_base: float = 2.0,
                 jitter: bool = True,
                 retry_on_exceptions: tuple = (Exception,)):
        
        self.max_attempts = max_attempts
        self.base_delay = base_delay
        self.max_delay = max_delay
        self.exponential_base = exponential_base
        self.jitter = jitter
        self.retry_on_exceptions = retry_on_exceptions

def retry_on_failure(config: Optional[RetryConfig] = None):
    """
    Decorator para retry automático em caso de falha
    
    Args:
        config: Configuração do retry (opcional)
        
    Returns:
        Função decorada com retry automático
    """
    
    if config is None:
        config = RetryConfig()
    
    def decorator(func: Callable) -> Callable:
        @wraps(func)
        def wrapper(*args, **kwargs) -> Any:
            last_exception = None
            
            for attempt in range(1, config.max_attempts + 1):
                try:
                    logger.debug(f"🔄 Tentativa {attempt}/{config.max_attempts} para {func.__name__}")
                    return func(*args, **kwargs)
                    
                except config.retry_on_exceptions as e:
                    last_exception = e
                    
                    if attempt == config.max_attempts:
                        logger.error(f"❌ {func.__name__} falhou após {config.max_attempts} tentativas: {e}")
                        raise
                    
                    # Calcular delay com backoff exponencial
                    delay = min(
                        config.base_delay * (config.exponential_base ** (attempt - 1)),
                        config.max_delay
                    )
                    
                    # Adicionar jitter para evitar thundering herd
                    if config.jitter:
                        delay = delay * (0.5 + random.random() * 0.5)
                    
                    logger.warning(f"⚠️ Tentativa {attempt} falhou: {e}")
                    logger.info(f"⏳ Aguardando {delay:.2f}s antes da próxima tentativa...")
                    
                    time.sleep(delay)
            
            # Nunca deve chegar aqui, mas por segurança
            if last_exception:
                raise last_exception
                
        return wrapper
    return decorator

def retry_network_operations(max_attempts: int = 3, base_delay: float = 2.0):
    """
    Decorator específico para operações de rede
    
    Args:
        max_attempts: Número máximo de tentativas
        base_delay: Delay base entre tentativas
        
    Returns:
        Função decorada com retry para operações de rede
    """
    
    config = RetryConfig(
        max_attempts=max_attempts,
        base_delay=base_delay,
        max_delay=30.0,
        exponential_base=2.0,
        jitter=True,
        retry_on_exceptions=(ConnectionError, TimeoutError, OSError)
    )
    
    return retry_on_failure(config)

def retry_selenium_operations(max_attempts: int = 3, base_delay: float = 1.0):
    """
    Decorator específico para operações do Selenium
    
    Args:
        max_attempts: Número máximo de tentativas
        base_delay: Delay base entre tentativas
        
    Returns:
        Função decorada com retry para operações do Selenium
    """
    
    # Importar aqui para evitar dependência circular
    from selenium.common.exceptions import (
        WebDriverException, 
        TimeoutException, 
        ElementClickInterceptedException,
        StaleElementReferenceException
    )
    
    config = RetryConfig(
        max_attempts=max_attempts,
        base_delay=base_delay,
        max_delay=10.0,
        exponential_base=1.5,
        jitter=True,
        retry_on_exceptions=(
            WebDriverException, 
            TimeoutException, 
            ElementClickInterceptedException,
            StaleElementReferenceException
        )
    )
    
    return retry_on_failure(config)

def retry_with_custom_strategy(
    max_attempts: int = 3,
    delay_strategy: str = 'exponential',
    base_delay: float = 1.0,
    max_delay: float = 60.0,
    retry_on_exceptions: tuple = (Exception,)
):
    """
    Decorator com estratégia de retry customizável
    
    Args:
        max_attempts: Número máximo de tentativas
        delay_strategy: Estratégia de delay ('exponential', 'linear', 'fixed')
        base_delay: Delay base
        max_delay: Delay máximo
        retry_on_exceptions: Exceções que devem gerar retry
        
    Returns:
        Função decorada com estratégia customizada
    """
    
    def decorator(func: Callable) -> Callable:
        @wraps(func)
        def wrapper(*args, **kwargs) -> Any:
            last_exception = None
            
            for attempt in range(1, max_attempts + 1):
                try:
                    logger.debug(f"🔄 Tentativa {attempt}/{max_attempts} para {func.__name__}")
                    return func(*args, **kwargs)
                    
                except retry_on_exceptions as e:
                    last_exception = e
                    
                    if attempt == max_attempts:
                        logger.error(f"❌ {func.__name__} falhou após {max_attempts} tentativas: {e}")
                        raise
                    
                    # Calcular delay baseado na estratégia
                    if delay_strategy == 'exponential':
                        delay = min(base_delay * (2 ** (attempt - 1)), max_delay)
                    elif delay_strategy == 'linear':
                        delay = min(base_delay * attempt, max_delay)
                    else:  # fixed
                        delay = base_delay
                    
                    # Adicionar jitter
                    delay = delay * (0.8 + random.random() * 0.4)
                    
                    logger.warning(f"⚠️ Tentativa {attempt} falhou: {e}")
                    logger.info(f"⏳ Aguardando {delay:.2f}s antes da próxima tentativa...")
                    
                    time.sleep(delay)
            
            if last_exception:
                raise last_exception
                
        return wrapper
    return decorator

# Funções utilitárias para retry manual
def retry_operation(operation: Callable, 
                   max_attempts: int = 3, 
                   base_delay: float = 1.0,
                   operation_name: str = "operação") -> Any:
    """
    Executa uma operação com retry automático
    
    Args:
        operation: Função a ser executada
        max_attempts: Número máximo de tentativas
        base_delay: Delay base entre tentativas
        operation_name: Nome da operação para logs
        
    Returns:
        Resultado da operação
        
    Raises:
        Exception: Se todas as tentativas falharem
    """
    
    last_exception = None
    
    for attempt in range(1, max_attempts + 1):
        try:
            logger.debug(f"🔄 Tentativa {attempt}/{max_attempts} para {operation_name}")
            return operation()
            
        except Exception as e:
            last_exception = e
            
            if attempt == max_attempts:
                logger.error(f"❌ {operation_name} falhou após {max_attempts} tentativas: {e}")
                raise
            
            delay = base_delay * (2 ** (attempt - 1))
            logger.warning(f"⚠️ Tentativa {attempt} falhou: {e}")
            logger.info(f"⏳ Aguardando {delay:.2f}s antes da próxima tentativa...")
            
            time.sleep(delay)
    
    if last_exception:
        raise last_exception

# Teste do sistema
if __name__ == "__main__":
    from config.logging_config import setup_logging
    
    # Configurar logging
    setup_logging(log_level=logging.DEBUG)
    
    # Teste de função com retry
    @retry_on_failure(RetryConfig(max_attempts=3, base_delay=0.1))
    def funcao_teste():
        import random
        if random.random() < 0.7:  # 70% de chance de falhar
            raise ValueError("Falha simulada")
        return "Sucesso!"
    
    # Teste
    try:
        resultado = funcao_teste()
        print(f"✅ Resultado: {resultado}")
    except Exception as e:
        print(f"❌ Falha final: {e}")
    
    print("✅ Sistema de retry testado com sucesso!")

