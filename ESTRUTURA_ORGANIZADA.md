# 📁 ESTRUTURA ORGANIZADA DO PROJETO

## 🗂️ Pastas Principais

### 📊 `dados_imoveis/`
- **Contém**: Todos os dados coletados dos imóveis (CSV e JSON)
- **Organização**: Por data (ex: `2025-07-17/`)
- **Arquivos**: `imoveis_[cidade]_[data].csv` e `imoveis_[cidade]_[data].json`

### 📋 `relatorios/`
- **Contém**: Relatórios gerados automaticamente
- **Organização**: Por data (ex: `2025-07-17/`)
- **Arquivos**: `relatorio_resumido_[data].txt` e `relatorio_detalhado_[data].txt`

### 🧪 `testes/`
- **Contém**: Scripts de teste e validação
- **Arquivos**: `teste_*.py`, `teste_email_robusto.py`, `teste_script_automatico.py`

### ⚙️ `config/`
- **Contém**: Arquivos de configuração
- **Arquivos**: `gmail_config_multiplos.json`, scripts de configuração

### 🖼️ `screenshots/`
- **Contém**: Imagens das páginas durante o scraping
- **Organização**: Por data (ex: `2025-07-17/`)

### 🗃️ `arquivos_antigos/`
- **Contém**: Notebooks, HTMLs e arquivos antigos

### 🛠️ `scripts/`
- **Contém**: Scripts utilitários e .bat

---

## 📧 Sistema de Email Múltiplo
- **Configuração**: `config/gmail_config_multiplos.json`
- **Gerencie destinatários**: `python config/configurar_gmail_multiplos.py`
- **Envio automático**: O `scraper_automatico.py` envia para todos os emails configurados

---

## 📝 Exemplo de Estrutura
```
📁 Projeto/
├── dados_imoveis/2025-07-17/
├── relatorios/2025-07-17/
├── screenshots/2025-07-17/
├── testes/
├── config/
├── scripts/
├── arquivos_antigos/
├── src/
├── README.md
├── ESTRUTURA_ORGANIZADA.md
└── ...
```

---

## 🚀 Fluxo de Uso
1. Configure os destinatários: `python config/configurar_gmail_multiplos.py`
2. Teste o envio: `python testes/teste_email_robusto.py`
3. Execute o scraper: `python scraper_automatico.py`

---

## 💡 Dicas
- Adicione/remova destinatários facilmente pelo configurador
- Os relatórios e dados são organizados automaticamente por data
- Consulte este arquivo sempre que tiver dúvidas sobre a estrutura 