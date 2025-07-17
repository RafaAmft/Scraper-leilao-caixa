# 🏠 Scraper Imóveis Caixa

Scraper interativo para extrair dados de imóveis do site da Caixa (https://venda-imoveis.caixa.gov.br/sistema/busca-imovel.asp?sltTipoBusca=imoveis).

## ✨ Funcionalidades

- 🔍 **Busca Interativa**: Interface amigável para configurar filtros
- 🏙️ **Múltiplas Cidades**: Suporte para SC, SP, RS, PR
- 💰 **Filtros Avançados**: Tipo de imóvel, faixa de valor, quartos
- 📊 **Exportação**: Dados salvos em CSV e JSON
- 📸 **Screenshots**: Capturas automáticas das páginas
- 🎯 **Dados Completos**: Endereço, valor, ID do imóvel, imagens

## 🚀 Instalação

### Windows
```bash
# Execute o instalador
install.bat
```

### Linux/Mac
```bash
# Torne o script executável
chmod +x install.sh

# Execute o instalador
./install.sh
```

### Instalação Manual
```bash
# Instalar dependências
pip install -r requirements.txt

# Instalar o projeto
pip install -e .
```

## 📋 Dependências

- **selenium**: Automação do navegador
- **pandas**: Manipulação de dados
- **webdriver-manager**: Gerenciamento automático do ChromeDriver
- **beautifulsoup4**: Parsing HTML
- **requests**: Requisições HTTP

## 🎮 Como Usar

### 🚀 Modo Rápido (Recomendado para uso frequente)
```bash
# Executar diretamente
python src/scraper_caixa/scraper.py

# Ou usar o arquivo .bat
executar_direto.bat
```

### 📦 Modo Completo (Após instalação)
```bash
# Instalar primeiro
install.bat

# Depois executar
busca-leilao-caixa

# Ou usar o arquivo .bat
executar_scraper.bat
```

### 🔧 Configuração Interativa
```bash
# Menu com opções
config_scraper.bat
```

## 🔧 Configuração

O scraper permite configurar:

### 📍 Estados Disponíveis
- **SC** (Santa Catarina)
- **SP** (São Paulo) 
- **RS** (Rio Grande do Sul)
- **PR** (Paraná)

### 🏙️ Cidades Principais
- **SC**: Joinville, Florianópolis, Blumenau, Brusque, Criciúma
- **SP**: São Paulo, Campinas, Santos, Ribeirão Preto
- **RS**: Porto Alegre, Caxias do Sul, Santa Maria, Pelotas
- **PR**: Curitiba, Londrina, Cascavel, Maringá

### 🏠 Tipos de Imóvel
- **1**: Casa
- **2**: Apartamento
- **4**: Indiferente

### 💰 Faixas de Valor
- **1**: Até R$ 50.000
- **2**: R$ 50.000 a R$ 100.000
- **3**: R$ 100.000 a R$ 150.000
- **4**: R$ 150.000 a R$ 200.000
- **5**: R$ 200.000 a R$ 300.000
- **6**: R$ 300.000 a R$ 500.000
- **7**: Acima de R$ 500.000

### 🛏️ Quartos
- **1**: 1 quarto
- **2**: 2 quartos
- **3**: 3 quartos
- **4**: 4+ quartos

## 📁 Arquivos Gerados

### Dados
- `imoveis_[estado]_[timestamp].csv` - Dados em formato CSV
- `imoveis_[estado]_[timestamp].json` - Dados em formato JSON

### Screenshots
- `screenshot_[estado]_[timestamp].png` - Captura da página

### Debug
- `pagina_sem_resultados_[estado]_[timestamp].html` - HTML para análise

## 📊 Exemplo de Saída

```
🎉 Total de imóveis encontrados: 3

📊 RESUMO DOS IMÓVEIS:
--------------------------------------------------
  1. COND RES PARK SUL
     Cidade: JOINVILLE
     Valor: R$ 111.168,79
     ID: 8444414000081

  2. COND RES ED PIEMONT
     Cidade: JOINVILLE
     Valor: R$ 220.000,00
     ID: 8555523293030

  3. COND PRIVILEGE
     Cidade: JOINVILLE
     Valor: R$ 282.967,55
     ID: 1555533963936
```

## 📧 **CONFIGURAÇÃO DE EMAIL**

### **Configurar Gmail (Recomendado)**
```bash
python config/configurar_gmail.py
```

### **Testar Envio de Email**
```bash
python config/teste_envio_email.py
```

### **Configuração Manual (Alternativa)**
```bash
python config/configurar_email.py
```

### **Testar Configuração**
```bash
python config/teste_scraper_automatico.py
```

## 🛠️ Scripts Disponíveis

### Principais
- `scraper_automatico.py` - Scraper automático com envio de email
- `scraper_simples_interativo.py` - Scraper interativo principal
- `scraper_caixa_final.py` - Scraper automático para Joinville
- `debug_site_caixa.py` - Script de debug para análise do site

### Utilitários
- `extrator_site_completo.py` - Extrator genérico de sites
- `analise_estrutura_caixa_final.py` - Análise da estrutura do site

## ⚠️ Requisitos

- **Python 3.8+**
- **Google Chrome** instalado
- **Conexão com internet**

## 🔍 Troubleshooting

### Erro de ChromeDriver
```bash
# Reinstalar webdriver-manager
pip install --upgrade webdriver-manager
```

### Nenhum imóvel encontrado
- Verifique se os filtros não estão muito restritivos
- Tente usar "Indiferente" para alguns filtros
- Verifique a conexão com a internet

### Erro de elemento não encontrado
- O site pode ter mudado a estrutura
- Execute o script de debug para análise

## 📝 Licença

MIT License - veja o arquivo LICENSE para detalhes.

## 🤝 Contribuição

1. Fork o projeto
2. Crie uma branch para sua feature (`git checkout -b feature/AmazingFeature`)
3. Commit suas mudanças (`git commit -m 'Add some AmazingFeature'`)
4. Push para a branch (`git push origin feature/AmazingFeature`)
5. Abra um Pull Request

## 📞 Suporte

Para dúvidas ou problemas:
- Abra uma issue no GitHub
- Verifique a documentação
- Execute o script de debug para análise

---

**Desenvolvido com ❤️ para facilitar a busca de imóveis da Caixa** 