# 📂 Scripts - Utilitários do Projeto

Esta pasta contém scripts auxiliares organizados por categoria.

## 📋 Estrutura

```
scripts/
├── verificacao/    # Scripts de verificação e diagnóstico
├── busca/          # Scripts para buscar códigos de cidades
├── testes/         # Scripts de teste local
└── antigos/        # Versões antigas (backup)
```

---

## 🔍 `/verificacao` - Verificação e Diagnóstico

Scripts para verificar códigos, visualizar configurações e diagnosticar problemas.

### Principais:
- **`verificar_codigos_df.py`** ⭐
  - Verifica códigos REAIS do DF no site da Caixa
  - Compara com configuração atual
  - Identifica códigos corretos/incorretos

- **`visualizar_cidades_df.py`** ⭐
  - Mostra todas as cidades configuradas
  - Destaque para o DF
  - Visualização formatada

- **`verificar_codigos_cidades.py`**
  - Verifica códigos de todas as cidades
  - Valida contra o site da Caixa

### Investigação:
- `investigar_*.py` (3 arquivos)
  - Investigar códigos de cidades
  - Investigar estrutura atual
  - Investigar site de leilões

### Debug:
- `debug_page_structure.py` - Analisa estrutura HTML
- `encontrar_url_correta.py` - Encontra URL correta do site
- `mostrar_cidades_configuradas.py` - Mostra config atual

---

## 🔎 `/busca` - Busca de Códigos

Scripts para encontrar códigos corretos de cidades no site da Caixa.

- **`buscar_cidades_desejadas.py`**
  - Busca códigos de cidades específicas
  
- **`buscar_codigos_cidades.py`**
  - Busca códigos gerais de cidades

- **`buscar_codigos_cidades_desejadas.py`**
  - Busca códigos de lista de cidades

- **`buscar_codigos_direto.py`**
  - Busca códigos diretamente do site

- **`buscar_codigos_sp_ms.py`**
  - Busca específica para SP e MS

- **`configurar_cidades_automatico.py`**
  - Configura cidades automaticamente

---

## 🧪 `/testes` - Scripts de Teste

Scripts para testar o scraper localmente antes de commitar.

### Testes Principais:
- **`teste_simples_ambiente.py`** ⭐
  - Teste básico do ambiente
  - Verifica ChromeDriver
  - Valida configuração

- **`teste_scraper_local.py`** ⭐
  - Testa scraper completo localmente
  - Executa busca real
  - Valida resultados

### Testes Específicos:
- `teste_busca_real.py` - Teste de busca real
- `teste_chrome_simples.py` - Teste simples do Chrome
- `teste_detalhado.py` - Teste detalhado com logs

### Testes de Endpoint:
- `testar_endpoint_cidades.py` - Testa endpoint de cidades
- `testar_endpoint_selenium.py` - Testa com Selenium

---

## 📦 `/antigos` - Versões Antigas

Backup de scripts antigos mantidos para referência.

- `scraper_automatico_antigo.py` - Versão antiga do scraper
- `scraper_direto.py` - Scraper direto (alternativa)

**Nota**: Estes arquivos **NÃO** devem ser usados. São mantidos apenas como referência histórica.

---

## 🚀 Como Usar

### Verificar Códigos do DF:
```bash
python scripts/verificacao/verificar_codigos_df.py
```

### Visualizar Todas as Cidades:
```bash
python scripts/verificacao/visualizar_cidades_df.py
```

### Testar Ambiente:
```bash
python scripts/testes/teste_simples_ambiente.py
```

### Testar Scraper Localmente:
```bash
python scripts/testes/teste_scraper_local.py
```

### Buscar Código de uma Cidade:
```bash
python scripts/busca/buscar_cidades_desejadas.py
```

---

## ⚠️ Importante

- **Scripts de verificação**: Seguros, podem ser executados a qualquer momento
- **Scripts de busca**: Acessam o site da Caixa, usar com moderação
- **Scripts de teste**: Executar antes de commits importantes
- **Scripts antigos**: NÃO usar, apenas referência

---

## 📝 Manutenção

Ao adicionar novos scripts:

1. ✅ Coloque na pasta apropriada
2. ✅ Atualize este README
3. ✅ Adicione docstring no script
4. ✅ Teste antes de commitar

---

**Última atualização**: 06/10/2025  
**Organização**: v1.1


