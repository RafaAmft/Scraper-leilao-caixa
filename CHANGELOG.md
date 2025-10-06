# Changelog

Todas as mudanças notáveis neste projeto serão documentadas neste arquivo.

O formato é baseado em [Keep a Changelog](https://keepachangelog.com/pt-BR/1.0.0/),
e este projeto adere ao [Semantic Versioning](https://semver.org/lang/pt-BR/).

## [1.1.0] - 2025-08-11

### ✨ Adicionado
- **Configuração moderna do projeto** (`pyproject.toml`)
- **Sistema de logging profissional** substituindo prints
- **Type hints** em todas as funções públicas
- **Exceções personalizadas** para melhor tratamento de erros
- **Módulo de configuração centralizada** (`config.py`)
- **Documentação aprimorada** com docstrings no padrão PEP 257
- **Requirements fixos** para reprodutibilidade
- **Suporte para desenvolvimento** (`requirements-dev.txt`)

### 🔧 Modificado
- **Estrutura do código** refatorada seguindo boas práticas
- **Imports organizados** seguindo PEP 8 (stdlib → terceiros → locais)
- **Separação de responsabilidades** em módulos específicos
- **Melhoria no tratamento de erros** com exceções específicas

### 📝 Documentação
- **Guia de boas práticas** (`boaspraticas.md`)
- **Docstrings completas** em todos os módulos
- **Type hints** para melhor IDE support
- **Este CHANGELOG** para rastrear mudanças

### 🏗️ Arquitetura
```
src/scraper_caixa/
├── __init__.py          # Exports organizados
├── config.py            # Configurações centralizadas
├── driver.py            # Gerenciamento do ChromeDriver
├── exceptions.py        # Exceções personalizadas
├── logger.py            # Sistema de logging
├── types.py             # Definições de tipos
└── scraper.py           # Lógica principal (a refatorar)
```

### 🧪 Testes
- Estrutura preparada para testes com pytest
- Configuração de cobertura mínima de 80%
- Suporte para testes unitários e de integração

### 📦 Dependências
- Versões fixas para garantir reprodutibilidade
- Separação entre dependências de produção e desenvolvimento
- Documentação clara de requisitos

---

## [1.0.0] - 2025-07-17

### Primeira versão funcional
- Scraper básico funcionando
- Suporte a múltiplas cidades
- Geração de relatórios
- Envio de emails
- GitHub Actions para automação

[1.1.0]: https://github.com/RafaAmft/Scraper-leilao-caixa/compare/v1.0.0...v1.1.0
[1.0.0]: https://github.com/RafaAmft/Scraper-leilao-caixa/releases/tag/v1.0.0

