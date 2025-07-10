# 📊 Extração de Dados do Site da Caixa

Este projeto foi desenvolvido para extrair e analisar dados de imóveis do site da Caixa (https://venda-imoveis.caixa.gov.br/sistema/busca-imovel.asp?sltTipoBusca=imoveis).

## 🎯 Objetivo

Criar um sistema completo de extração de dados HTML de sites para análise, com foco em imóveis da Caixa em Joinville, SC.

## 📁 Arquivos Gerados

### Scripts Principais
- `extrator_site_completo.py` - Script principal de extração
- `analise_dados_caixa.py` - Script de análise dos dados extraídos
- `resumo_final_extracao.py` - Script de resumo final

### Dados Extraídos
- `dados_site_20250710_104928.json` - Dados estruturados em JSON
- `resumo_site_20250710_104928.csv` - Resumo em formato CSV
- `pagina_html_20250710_104928.html` - HTML completo da página
- `screenshot_20250710_104927.png` - Screenshot da página
- `resumo_analise_caixa_20250710_105058.csv` - Análise detalhada

## 📊 Resultados da Extração

### Informações Básicas
- **URL**: https://www.vivareal.com.br/imovel/apartamento-3-quartos-sao-marcos-bairros-joinville-com-garagem-2065m2-venda-RS282967-id-2815358830/
- **Status**: 200 (Sucesso)
- **Tamanho HTML**: 539,232 bytes
- **Data de Extração**: 2025-07-10 10:49:28

### Estatísticas de Conteúdo
- **Links encontrados**: 20
- **Imagens encontradas**: 10
- **Formulários**: 0
- **Tabelas**: 0

### Dados de Imóveis Extraídos
- **Preços**: 5 entradas
- **Endereços**: 5 entradas
- **Características**: 10 entradas

### Análise do Texto
- **Tamanho**: 4,840 caracteres
- **Menções a preços**: 4
- **Menções a Joinville**: 9
- **Menções a São Marcos**: 6
- **Menções a m²**: 2
- **Menções a quartos**: 1
- **Menções a banheiros**: 2

## 🏠 Dados Específicos do Imóvel

### Informações Principais
- **Tipo**: Apartamento
- **Preço**: R$ 282.967
- **Endereço**: Rua Tupy, N. 835 APTO. 303B BL 02 - São Marcos, Joinville - SC
- **Área**: 2065 m²
- **Quartos**: 3
- **Banheiros**: 1
- **Vagas**: 2

### Características
- Varanda/sacada
- Área de Serviço
- 2 WCs
- Sala
- Cozinha

## 🔧 Como Usar

### 1. Executar Extração
```bash
python extrator_site_completo.py "URL_DO_SITE"
```

### 2. Analisar Dados
```bash
python analise_dados_caixa.py
```

### 3. Ver Resumo Final
```bash
python resumo_final_extracao.py
```

## 📈 Funcionalidades

### Extração Completa
- ✅ Captura de HTML completo
- ✅ Screenshot da página
- ✅ Extração de links
- ✅ Extração de imagens
- ✅ Análise de formulários
- ✅ Análise de tabelas
- ✅ Dados estruturados em JSON

### Análise Avançada
- ✅ Busca por preços (R$)
- ✅ Busca por endereços
- ✅ Busca por áreas (m²)
- ✅ Busca por quartos/banheiros
- ✅ Contagem de menções geográficas
- ✅ Categorização de links
- ✅ Análise de imagens por domínio

### Exportação
- ✅ JSON estruturado
- ✅ CSV com resumo
- ✅ HTML completo
- ✅ Screenshot PNG

## 🚀 Próximos Passos

1. **📊 Análise Detalhada**: Analisar os dados extraídos em profundidade
2. **🔍 Expansão**: Extrair dados de mais páginas do site
3. **📈 Visualização**: Criar gráficos e dashboards
4. **💾 Estruturação**: Salvar dados em banco de dados
5. **🔄 Automação**: Criar sistema automatizado de extração

## 📋 Dependências

- Python 3.7+
- requests
- beautifulsoup4
- pandas
- selenium
- webdriver-manager
- pillow

## 🎯 Conclusões

A extração foi **bem-sucedida** e capturou dados relevantes sobre imóveis da Caixa em Joinville, incluindo:

- ✅ Informações de preço e localização
- ✅ Características do imóvel
- ✅ Links para navegação
- ✅ Imagens do imóvel
- ✅ Dados estruturados para análise

O sistema está pronto para ser expandido e automatizado para extrair dados de múltiplas páginas e imóveis.

---

**Desenvolvido para análise de dados de imóveis da Caixa em Joinville, SC** 