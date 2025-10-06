"""
Exceções personalizadas do scraper.

Seguindo boas práticas, usa exceções específicas em vez de genéricas.
"""


class ScraperError(Exception):
    """Exceção base para erros do scraper."""
    
    pass


class ChromeDriverError(ScraperError):
    """Erro na configuração ou execução do ChromeDriver."""
    
    pass


class NavigationError(ScraperError):
    """Erro ao navegar entre páginas."""
    
    pass


class ElementNotFoundError(ScraperError):
    """Elemento HTML não encontrado na página."""
    
    pass


class DataExtractionError(ScraperError):
    """Erro ao extrair dados da página."""
    
    pass


class ValidationError(ScraperError):
    """Erro na validação de dados."""
    
    pass


class ConfigurationError(ScraperError):
    """Erro na configuração do scraper."""
    
    pass


class TimeoutError(ScraperError):
    """Timeout ao aguardar elemento ou operação."""
    
    pass

