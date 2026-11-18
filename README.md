# 🏠 Scraper Imóveis Caixa

Scraper interativo para extrair dados de imóveis do site da Caixa (https://venda-imoveis.caixa.gov.br/sistema/busca-imovel.asp?sltTipoBusca=imoveis).

## ✨ Funcionalidades

- 🔍 **Busca Interativa**: Interface amigável para configurar filtros
- 🏙️ **Múltiplas Cidades**: Suporte para SC, SP, RS, PR
- 💰 **Filtros Avançados**: Tipo de imóvel, faixa de valor, quartos
- 📊 **Exportação**: Dados salvos em CSV e JSON
- 📸 **Screenshots**: Capturas automáticas das páginas
- 🎯 **Dados Completos**: Endereço, valor, ID do imóvel, imagens
- 📧 **Envio de Email para Múltiplos Destinatários**

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

### 🚀 Modo Automático Completo
```bash
python scraper_automatico.py
```

- Busca imóveis em todas as cidades configuradas
- Gera relatórios e envia para todos os destinatários cadastrados

### 🛡️ Download do CSV (proteção Radware da Caixa)

O site da Caixa usa o **Radware Bot Manager**, que bloqueia downloads feitos por scripts
(inclusive no GitHub Actions). Por isso o script tenta, em ordem (`--metodo auto`):

1. **requests**: download HTTP direto (costuma ser bloqueado);
2. **navegador**: Google Chrome real via Playwright, com perfil salvo em `navegador_perfil/`;
3. **downloads**: o `Lista_imoveis_geral*.csv` mais recente (últimas 24h) da sua pasta Downloads.

Preparação (uma vez):
```bash
pip install -r requirements.txt
playwright install chromium   # só é necessário se o Google Chrome não estiver instalado
```

Primeira execução, **com a janela do navegador visível**:
```bash
python scraper_automatico.py --metodo navegador --sem-email
```
Se aparecer um captcha, resolva-o na janela; o download continua sozinho. Os cookies de
liberação ficam salvos em `navegador_perfil/` (não versionado) e são reaproveitados nas
próximas execuções.

Para rodar sem a janela atrapalhar (ex.: Agendador de Tarefas), use uma das opções:
- `--janela-escondida`: Chrome com janela, mas fora da área visível da tela (**recomendado**,
  para o site é um navegador comum);
- `--headless`: Chrome sem janela. O script disfarça o User-Agent `HeadlessChrome`, mas a
  proteção pode detectar o modo headless por outros sinais; nesse caso desiste em 45s.

Se mesmo assim for bloqueado, baixe o arquivo manualmente em
<https://venda-imoveis.caixa.gov.br/sistema/download-lista.asp> e rode
`python scraper_automatico.py` (ele encontra o CSV na pasta Downloads) ou use `--csv <caminho>`.

Outras opções: `--perfil-navegador <pasta>`, `--pasta-downloads <pasta>`.

### 📊 Painel de imóveis (Brasil inteiro)

A cada execução o scraper gera **`painel_imoveis.html`** com **todos os imóveis da lista
da Caixa** (não só as cidades monitoradas). É um arquivo único, que abre em qualquer
navegador e funciona offline:

- **Métricas gerais:** total de imóveis, preço mediano, desconto mediano, preço mediano
  por m² e % que aceita financiamento — recalculadas conforme os filtros;
- **Gráficos:** imóveis por estado, cidades com mais imóveis, modalidade de venda e faixa
  de desconto (clique em uma barra para filtrar);
- **Filtros:** estado, cidade, tipo, modalidade, preço máximo, desconto mínimo, quartos,
  financiamento, busca por bairro/endereço e "só cidades monitoradas";
- **Tabela** ordenável com link para cada imóvel no site da Caixa e **exportação CSV**
  do resultado filtrado; tema claro/escuro.

```bash
python scraper_automatico.py --abrir-painel          # gera e abre no navegador
python scraper_automatico.py --csv dados_imoveis/Lista_imoveis_geral.csv --sem-email --abrir-painel
```
Opções: `--painel <arquivo>` (outro nome/pasta) e `--sem-painel` (não gera).

### ⏰ Execução diária no Windows (Agendador de Tarefas)

O GitHub Actions é bloqueado pela proteção da Caixa, então a rotina diária roda no seu PC.

1. Rode uma vez manualmente e confira o envio do e-mail:
   ```powershell
   python scraper_automatico.py --metodo navegador --headless
   ```
   (se pedir credencial do Gmail: `python scraper_automatico.py --auth-gmail`)
2. Crie a tarefa diária (horário opcional, padrão 08:00):
   ```powershell
   scripts\criar_tarefa_agendada.bat 08:00
   ```
3. Teste na hora: `schtasks /Run /TN "Scraper Leilao Caixa"` e veja `logs\agendador.log`.

A tarefa executa `scripts\agendar_scraper.bat`, que roda
`scraper_automatico.py --metodo auto --headless` (usando `.venv` ou `venv` do projeto, se
existir) e grava toda a saída em `logs\agendador.log`. Ela roda com o seu usuário conectado;
se o PC estiver desligado no horário, roda assim que for ligado. Uma janela de console
aparece rapidamente durante a execução.

Se um dia o log mostrar bloqueio (cookies da Caixa expirados), rode uma vez com janela
(`python scraper_automatico.py --metodo navegador --sem-email`) para renová-los.

Para remover a tarefa: `schtasks /Delete /TN "Scraper Leilao Caixa" /F`.

### 🔧 Configuração Interativa
```bash
# Menu com opções
config_scraper.bat
```

## ⚙️ Configuração

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

## 📁 Estrutura de Pastas

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

- **dados_imoveis/**: Dados CSV/JSON organizados por data
- **relatorios/**: Relatórios resumidos e detalhados por data
- **screenshots/**: Imagens das páginas por data
- **config/**: Configurações do sistema e email
- **testes/**: Scripts de teste e validação
- **scripts/**: Scripts utilitários e .bat
- **arquivos_antigos/**: Notebooks, HTMLs e arquivos antigos

## 📧 **CONFIGURAÇÃO DE EMAIL MÚLTIPLO**

### **Configurar Destinatários**
```bash
python config/configurar_gmail_multiplos.py
```
- Adicione/remova destinatários facilmente
- O arquivo de configuração é `config/gmail_config_multiplos.json`

### **Testar Envio de Email**
```bash
python testes/teste_email_robusto.py
```

### **Envio Automático**
- O `scraper_automatico.py` envia o relatório para todos os emails cadastrados

## 📁 Arquivos Gerados

### Dados
- `imoveis_[cidade]_[data].csv` - Dados em formato CSV
- `imoveis_[cidade]_[data].json` - Dados em formato JSON

### Screenshots
- `screenshot_[cidade]_[data].png` - Captura da página

### Relatórios
- `relatorio_resumido_[data].txt` - Resumo do dia
- `relatorio_detalhado_[data].txt` - Detalhamento completo

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

## 🛠️ Scripts Disponíveis

### Principais
- `scraper_automatico.py` - Scraper automático com envio de email múltiplo
- `testes/teste_email_robusto.py` - Teste robusto de envio de email
- `testes/teste_script_automatico.py` - Teste do fluxo automático para uma cidade

### Utilitários
- `config/configurar_gmail_multiplos.py` - Configuração de múltiplos destinatários
- `configuracao_cidades.json` - Configuração das cidades monitoradas

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