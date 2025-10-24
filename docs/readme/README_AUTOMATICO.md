# 🚀 Scraper Automático de Imóveis - Caixa

Este sistema automatiza a busca de imóveis em múltiplas cidades do site da Caixa e envia relatórios diários por email.

## 📋 Cidades Configuradas

### Santa Catarina (SC)
- ✅ Joinville (código: 8690)
- ✅ Blumenau (código: 8545)
- ⚠️ Barra Velha (código: 8500) - Aproximado
- ⚠️ Balneário Piçarras (código: 8510) - Aproximado
- ⚠️ Itajaí (código: 8520) - Aproximado
- ⚠️ Governador Celso Ramos (código: 8530) - Aproximado

### Mato Grosso do Sul (MS)
- ✅ Campo Grande (código: 5002704)

### São Paulo (SP)
- ✅ São Paulo (código: 3550308)
- ⚠️ São José do Rio Preto (código: 3550000) - Aproximado
- ⚠️ Bady Bassit (código: 3550100) - Aproximado

## ⚙️ Configuração

### 1. Configurar Email

Edite o arquivo `scraper_automatico.py` e altere as seguintes linhas:

```python
EMAIL_REMETENTE = "seu_email@gmail.com"  # ⚠️ ALTERAR
EMAIL_DESTINATARIO = "destinatario@email.com"  # ⚠️ ALTERAR
SENHA_APP = "sua_senha_de_app"  # ⚠️ ALTERAR
```

**Para Gmail:**
1. Ative a verificação em duas etapas
2. Gere uma senha de app: https://myaccount.google.com/apppasswords
3. Use essa senha no campo `SENHA_APP`

### 2. Testar o Sistema

Execute o script para testar:

```bash
python scraper_automatico.py
```

## ⏰ Agendamento Automático

### Windows - Agendador de Tarefas

1. Abra o "Agendador de Tarefas" (Task Scheduler)
2. Clique em "Criar Tarefa Básica"
3. Configure:
   - **Nome**: Scraper Imóveis Caixa
   - **Descrição**: Busca automática de imóveis
   - **Frequência**: Diariamente
   - **Hora de início**: 08:00
   - **Ação**: Iniciar um programa
   - **Programa**: `executar_scraper_automatico.bat`
   - **Iniciar em**: `C:\caminho\para\seu\projeto`

### Configuração Avançada

Para configuração mais detalhada:

1. **Propriedades da Tarefa**:
   - Marque "Executar com privilégios mais altos"
   - Em "Configurações", marque "Executar a tarefa assim que possível se uma execução for perdida"

2. **Condições**:
   - Desmarque "Iniciar a tarefa apenas se o computador estiver em uso"
   - Marque "Parar se o computador mudar para modo de bateria"

## 📊 Arquivos Gerados

### Relatórios
- `relatorio_YYYYMMDD_HHMMSS.txt` - Relatório detalhado de cada execução

### Dados
- `imoveis_[cidade]_[timestamp].csv` - Dados em CSV
- `imoveis_[cidade]_[timestamp].json` - Dados em JSON

### Screenshots
- `screenshot_[cidade]_[timestamp].png` - Capturas das páginas

## 🔧 Troubleshooting

### Erro de ChromeDriver
```bash
pip install --upgrade webdriver-manager
```

### Erro de Email
- Verifique se a senha de app está correta
- Confirme se a verificação em duas etapas está ativa
- Teste o envio manual primeiro

### Códigos de Cidade Incorretos
Se alguma cidade não for encontrada, edite `configuracao_cidades.json` e corrija o código.

## 📧 Exemplo de Relatório

```
📊 RELATÓRIO DIÁRIO DE IMÓVEIS - CAIXA
Data: 15/01/2025 08:00
Cidades processadas: 9
Total de imóveis encontrados: 45

🏙️ JOINVILLE/SC: 12 imóveis encontrados
  1. RESIDENCIAL JARDIM EUROPA - R$ 150.000,00
  2. APARTAMENTO CENTRO - R$ 200.000,00
  ... e mais 10 imóveis

🏙️ BLUMENAU/SC: 8 imóveis encontrados
  1. CASA VILA NOVA - R$ 180.000,00
  2. APARTAMENTO GARCIA - R$ 220.000,00
  ... e mais 6 imóveis

---
Relatório gerado automaticamente
```

## 🎯 Próximos Passos

1. ✅ Configurar email
2. ✅ Testar o script
3. ✅ Configurar agendamento
4. 🔄 Monitorar execuções
5. 🔄 Ajustar códigos de cidade se necessário

## 📞 Suporte

Para problemas ou dúvidas:
- Verifique os logs de erro
- Teste manualmente primeiro
- Confirme se o Chrome está atualizado
- Verifique a conexão com internet 