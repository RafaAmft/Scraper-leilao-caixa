#!/usr/bin/env python3
"""
Configuração de ambiente para o Scraper Imóveis Caixa
"""

import os
from typing import Dict, Any

class EnvironmentConfig:
    """Configuração de ambiente do projeto"""
    
    # Configurações padrão
    DEFAULT_CONFIG = {
        'LOG_LEVEL': 'INFO',
        'LOG_TO_FILE': True,
        'LOG_TO_CONSOLE': True,
        'MAX_RETRY_ATTEMPTS': 3,
        'RETRY_DELAY': 5,
        'REQUEST_TIMEOUT': 30,
        'CHROME_HEADLESS': True,
        'CHROME_WINDOW_SIZE': '1920,1080',
        'PAUSE_BETWEEN_CITIES': 5,
        'PAUSE_BETWEEN_PAGES': 3,
        'MAX_PAGES_PER_CITY': 50,
        'EMAIL_TIMEOUT': 60,
        'DATA_VALIDATION_ENABLED': True,
        'SCREENSHOT_ENABLED': True,
        'BACKUP_ENABLED': True
    }
    
    @classmethod
    def get_config(cls) -> Dict[str, Any]:
        """Retorna configuração do ambiente"""
        config = cls.DEFAULT_CONFIG.copy()
        
        # Sobrescrever com variáveis de ambiente se existirem
        for key in config.keys():
            env_value = os.getenv(f'SCRAPER_{key}')
            if env_value is not None:
                # Converter tipos apropriados
                if env_value.lower() in ('true', 'false'):
                    config[key] = env_value.lower() == 'true'
                elif env_value.isdigit():
                    config[key] = int(env_value)
                elif env_value.replace('.', '').isdigit():
                    config[key] = float(env_value)
                else:
                    config[key] = env_value
        
        return config
    
    @classmethod
    def get_log_level(cls) -> str:
        """Retorna nível de log configurado"""
        return cls.get_config()['LOG_LEVEL']
    
    @classmethod
    def is_headless(cls) -> bool:
        """Retorna se o Chrome deve rodar em modo headless"""
        return cls.get_config()['CHROME_HEADLESS']
    
    @classmethod
    def get_retry_config(cls) -> Dict[str, Any]:
        """Retorna configuração de retry"""
        config = cls.get_config()
        return {
            'max_attempts': config['MAX_RETRY_ATTEMPTS'],
            'base_delay': config['RETRY_DELAY']
        }
    
    @classmethod
    def get_timeout_config(cls) -> Dict[str, Any]:
        """Retorna configuração de timeouts"""
        config = cls.get_config()
        return {
            'request_timeout': config['REQUEST_TIMEOUT'],
            'email_timeout': config['EMAIL_TIMEOUT']
        }

# Configurações específicas por ambiente
class DevelopmentConfig(EnvironmentConfig):
    """Configuração para desenvolvimento"""
    
    DEFAULT_CONFIG = EnvironmentConfig.DEFAULT_CONFIG.copy()
    DEFAULT_CONFIG.update({
        'LOG_LEVEL': 'DEBUG',
        'CHROME_HEADLESS': False,
        'PAUSE_BETWEEN_CITIES': 2,
        'PAUSE_BETWEEN_PAGES': 1,
        'MAX_PAGES_PER_CITY': 5
    })

class ProductionConfig(EnvironmentConfig):
    """Configuração para produção"""
    
    DEFAULT_CONFIG = EnvironmentConfig.DEFAULT_CONFIG.copy()
    DEFAULT_CONFIG.update({
        'LOG_LEVEL': 'WARNING',
        'CHROME_HEADLESS': True,
        'PAUSE_BETWEEN_CITIES': 10,
        'PAUSE_BETWEEN_PAGES': 5,
        'MAX_PAGES_PER_CITY': 100
    })

# Função para obter configuração baseada no ambiente
def get_environment_config() -> EnvironmentConfig:
    """Retorna configuração baseada no ambiente atual"""
    env = os.getenv('SCRAPER_ENV', 'development').lower()
    
    if env == 'production':
        return ProductionConfig()
    else:
        return DevelopmentConfig()

# Configuração global
config = get_environment_config()

