# 🏠 Scraper de Imóveis da Caixa v1.1

[![Python Version](https://img.shields.io/badge/python-3.10%2B-blue)](https://www.python.org/downloads/)
[![Code Style](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)
[![License](https://img.shields.io/badge/license-MIT-green.svg)](LICENSE)

> Scraper automatizado e profissional para buscar imóveis em leilão da Caixa Econômica Federal.

---

## 📋 Índice

- [Sobre](#sobre)
- [Novidades v1.1](#novidades-v11)
- [Instalação](#instalação)
- [Uso Básico](#uso-básico)
- [Arquitetura](#arquitetura)
- [Desenvolvimento](#desenvolvimento)
- [Contribuindo](#contribuindo)
- [Licença](#licença)

---

## 🎯 Sobre

Este projeto realiza scraping automatizado de imóveis em leilão da **Caixa Econômica Federal**, extraindo informações como:

- 🏘️ Nome do imóvel
- 📍 Endereço completo
- 💰 Valor de avaliação
- 🛏️ Número de quartos
- 🔗 Link direto para o imóvel

### Principais Recursos

✅ **Automatização completa** com Selenium  
✅ **Multi-cidades** - busca em várias cidades simultaneamente  
✅ **Anti-detecção** - configurado para evitar bloqueios  
✅ **Relatórios** - gera CSV, JSON e relatórios de texto  
✅ **Screenshots** - captura tela de cada busca  
✅ **Logging profissional** - rastreabilidade completa  
✅ **Type-safe** - type hints em todo o código  
✅ **Testável** - arquitetura modular preparada para testes  

---

## ✨ Novidades v1.1

### 🏗️ **Refatoração Completa**

A versão 1.1 traz uma refatoração profunda seguindo **boas práticas de código**:

#### Arquitetura Modular
```
src/scraper_caixa/
├── config.py         # Configurações centralizadas
├── driver.py         # Gerenciamento do ChromeDriver
├── exceptions.py     # Exceções personalizadas
├── logger.py         # Sistema de logging
├── types.py          # Type hints e definições
└── scraper.py        # Lógica principal
```

#### Melhorias Técnicas
- ✅ **PEP 8** - código formatado com Black
- ✅ **Type Hints** - tipagem completa
- ✅ **Logging** - substituição de prints
- ✅ **Docstrings** - documentação PEP 257
- ✅ **Configuração** - separada de código
- ✅ **Exceções** - hierarquia específica

#### Configuração Moderna
- ✅ `pyproject.toml` - configuração centralizada
- ✅ Dependências fixas - reprodutibilidade
- ✅ Dev tools - black, mypy, pytest

Veja detalhes em [CHANGELOG.md](CHANGELOG.md) e [REFATORACAO_V1.1.md](REFATORACAO_V1.1.md).

---

## 📦 Instalação

### Requisitos
- Python 3.10 ou superior
- Google Chrome instalado
- pip

### Instalação Básica

```bash
# Clonar repositório
git clone https://github.com/RafaAmft/Scraper-leilao-caixa.git
cd Scraper-leilao-caixa

# Instalar dependências
pip install -r requirements.txt

# Ou instalar em modo desenvolvimento
pip install -e ".[dev]"
```

### Verificar Instalação

```bash
python -c "from scraper_caixa import __version__; print(__version__)"
# Deve exibir: 1.1.0
```

---

## 🚀 Uso Básico

### Exemplo Simples

```python
from scraper_caixa import (
    configurar_chromedriver,
    ScraperConfig,
    get_logger,
    FiltrosBusca,
)

# Configurar logger
logger = get_logger(__name__)

# Configurar scraper
config = ScraperConfig(
    headless=True,
    save_screenshots=True,
    save_json=True,
)

# Configurar driver
driver = configurar_chromedriver(config)

# Definir filtros de busca
filtros: FiltrosBusca = {
    "estado": "SC",
    "codigo_cidade": "8690",
    "nome_cidade": "JOINVILLE",
    "tipo_imovel": "4",  # Indiferente
}

# Executar busca
# (implementação do scraper em desenvolvimento)

# Fechar driver
driver.quit()
```

### Configuração Personalizada

```python
from scraper_caixa.config import ScraperConfig
from pathlib import Path

config = ScraperConfig(
    headless=False,           # Ver navegador
    timeout=60,               # Timeout maior
    max_retries=5,            # Mais tentativas
    save_screenshots=True,
    data_dir=Path("./meus_dados"),
)
```

---

## 🏗️ Arquitetura

### Módulos Principais

#### 1. `config.py` - Configurações
```python
from scraper_caixa.config import (
    URL_BASE,
    CHROME_OPTIONS,
    ESTADOS_CIDADES,
    ScraperConfig,
)
```

#### 2. `driver.py` - ChromeDriver
```python
from scraper_caixa.driver import configurar_chromedriver

driver = configurar_chromedriver()
```

#### 3. `logger.py` - Logging
```python
from scraper_caixa.logger import get_logger

logger = get_logger(__name__)
logger.info("Mensagem de log")
```

#### 4. `exceptions.py` - Exceções
```python
from scraper_caixa.exceptions import (
    ScraperError,
    ChromeDriverError,
    NavigationError,
)

try:
    # código
    pass
except ChromeDriverError as e:
    logger.error(f"Erro: {e}")
```

#### 5. `types.py` - Type Hints
```python
from scraper_caixa.types import FiltrosBusca, DadosImovel

filtros: FiltrosBusca = {
    "estado": "SC",
    "codigo_cidade": "8690",
}
```

---

## 🛠️ Desenvolvimento

### Setup Ambiente de Desenvolvimento

```bash
# Instalar dependências de desenvolvimento
pip install -r requirements-dev.txt

# Instalar pre-commit hooks (recomendado)
pre-commit install
```

### Ferramentas de Qualidade

#### Formatação de Código
```bash
# Formatar com Black
black src/ tests/

# Ordenar imports com isort
isort src/ tests/
```

#### Verificação de Estilo
```bash
# Verificar com flake8
flake8 src/ tests/

# Verificar tipos com mypy
mypy src/
```

#### Testes
```bash
# Executar testes (quando implementados)
pytest

# Com cobertura
pytest --cov=src --cov-report=html
```

### Estrutura de Diretórios

```
projeto/
├── src/scraper_caixa/        # Código fonte
├── tests/                     # Testes unitários
├── docs/                      # Documentação
├── dados_imoveis/             # Dados extraídos
├── screenshots/               # Capturas de tela
├── relatorios/                # Relatórios gerados
├── logs/                      # Arquivos de log
├── pyproject.toml             # Configuração do projeto
├── requirements.txt           # Dependências produção
└── requirements-dev.txt       # Dependências desenvolvimento
```

---

## 📚 Documentação Adicional

- 📘 [Boas Práticas](boaspraticas.md) - Guia de boas práticas
- 📝 [Changelog](CHANGELOG.md) - Histórico de mudanças
- 🔧 [Refatoração v1.1](REFATORACAO_V1.1.md) - Detalhes da refatoração
- 📊 [Resumo](RESUMO_REFATORACAO.md) - Resumo executivo

---

## 🤝 Contribuindo

Contribuições são bem-vindas! Para contribuir:

1. Fork o projeto
2. Crie uma branch (`git checkout -b feature/MinhaFeature`)
3. Commit suas mudanças (`git commit -m 'feat: Adicionar feature'`)
4. Push para a branch (`git push origin feature/MinhaFeature`)
5. Abra um Pull Request

### Padrões

- Seguir [PEP 8](https://peps.python.org/pep-0008/)
- Usar [Conventional Commits](https://www.conventionalcommits.org/)
- Adicionar testes para novas features
- Atualizar documentação

---

## 📄 Licença

Este projeto está sob a licença MIT. Veja [LICENSE](LICENSE) para mais detalhes.

---

## 👤 Autor

**Rafael Fontes**
- Email: rafael.a.fontes@hotmail.com
- GitHub: [@RafaAmft](https://github.com/RafaAmft)

---

## 🙏 Agradecimentos

- Comunidade Python
- Selenium WebDriver
- Todos os contribuidores

---

## 📞 Suporte

Encontrou um bug? Tem uma sugestão?

- 🐛 [Abra uma issue](https://github.com/RafaAmft/Scraper-leilao-caixa/issues)
- 💬 [Inicie uma discussão](https://github.com/RafaAmft/Scraper-leilao-caixa/discussions)

---

**⭐ Se este projeto te ajudou, considere dar uma estrela!**

---

Feito com ❤️ e ☕ por Rafael Fontes

