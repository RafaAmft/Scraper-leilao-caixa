# 🔄 Configuração CI/CD - GitHub Actions

## 📋 Workflows Configurados

### 1. 🏠 **Scraper Diário** (`scraper-daily.yml`)

**Função**: Executa o scraper automaticamente todos os dias

#### ⏰ Agendamento
- **Frequência**: 1 vez por dia
- **Horário**: 8h UTC (5h Brasília)
- **Cron**: `0 8 * * *`

#### 🎯 O que faz:
1. ✅ Configura ambiente Python 3.10
2. ✅ Instala dependências
3. ✅ Instala Google Chrome
4. ✅ Executa `scraper_automatico.py`
5. ✅ Verifica arquivos gerados
6. ✅ Faz upload dos resultados
7. ✅ Gera resumo da execução

#### 📤 Resultados Salvos:
- `relatorio_*.txt` - Relatórios de texto
- `imoveis_*.json` - Dados em JSON
- `imoveis_*.csv` - Dados em CSV
- `screenshot_*.png` - Capturas de tela
- `*.log` - Logs de execução

**Retenção**: 30 dias

#### 🎮 Execução Manual:
Você pode executar manualmente a qualquer momento:
1. Vá para: https://github.com/RafaAmft/Scraper-leilao-caixa/actions
2. Selecione "🏠 Scraper Diário de Imóveis"
3. Clique em "Run workflow"

---

### 2. 🧪 **Teste Simples** (`test-simples.yml`)

**Função**: Testa o ambiente e módulos básicos

#### ⚡ Quando executa:
- ✅ Em pull requests para `main`
- ✅ Em push para `main`
- ✅ Manualmente (workflow_dispatch)

#### 🎯 O que testa:
1. ✅ Importação de módulos refatorados
2. ✅ Configuração do ChromeDriver
3. ✅ Sistema de logging
4. ✅ Navegação básica

**Tempo**: ~5 minutos

---

## 📅 Horários de Execução

### Horário UTC vs Brasília

| Evento | UTC | Brasília (GMT-3) |
|--------|-----|------------------|
| Scraper Diário | 8h | 5h |

### 🔧 Como Alterar o Horário

Para mudar o horário de execução do scraper, edite o arquivo `.github/workflows/scraper-daily.yml`:

```yaml
schedule:
  - cron: '0 8 * * *'  # Formato: minuto hora dia mês dia-da-semana
```

#### Exemplos de Cron:
```yaml
# Às 10h UTC (7h Brasília)
- cron: '0 10 * * *'

# Às 12h UTC (9h Brasília)
- cron: '0 12 * * *'

# Às 14h UTC (11h Brasília)
- cron: '0 14 * * *'

# Duas vezes por dia (8h e 20h UTC)
- cron: '0 8,20 * * *'

# Apenas dias úteis às 8h UTC
- cron: '0 8 * * 1-5'
```

---

## 📊 Monitoramento

### Ver Execuções
1. Acesse: https://github.com/RafaAmft/Scraper-leilao-caixa/actions
2. Selecione o workflow desejado
3. Veja histórico e logs

### Baixar Resultados
1. Entre em uma execução específica
2. Role até "Artifacts"
3. Baixe `resultados-scraper-XXX.zip`

### Ver Resumo
Cada execução gera um resumo automático com:
- 📊 Número de arquivos gerados
- ✅ Status de sucesso
- 📝 Estatísticas

---

## 🔔 Notificações

### Configurar Notificações por Email

1. **Configurações do Repositório**:
   - Vá em Settings → Notifications
   - Configure suas preferências

2. **Watch o Repositório**:
   - Clique em "Watch" no topo
   - Selecione "Custom"
   - Marque "Actions"

### Notificações de Falha

O workflow envia notificação automática se:
- ❌ O scraper falha completamente
- ⚠️ Nenhum arquivo é gerado
- 🚨 Timeout (30 minutos)

---

## 🛠️ Manutenção

### Desabilitar Execução Automática

Para pausar a execução diária temporariamente:

1. **Opção 1**: Comentar o schedule no arquivo
```yaml
# schedule:
#   - cron: '0 8 * * *'
```

2. **Opção 2**: Desabilitar workflow no GitHub
   - Actions → Workflow → "..." → Disable workflow

### Reativar
- Descomentar o schedule
- Ou: Enable workflow no GitHub

---

## 📈 Otimizações

### Cache de Dependências
O workflow usa cache do pip para acelerar instalação:
```yaml
- uses: actions/setup-python@v4
  with:
    cache: 'pip'  # ✅ Cache habilitado
```

### Timeout
Tempo máximo de execução: 30 minutos
```yaml
timeout-minutes: 30
```

Se precisar de mais tempo, aumente este valor.

---

## 🔍 Troubleshooting

### Problema: Workflow não executa

**Soluções**:
1. Verificar se está habilitado em Actions
2. Confirmar syntax do cron
3. Ver se há commits recentes

### Problema: ChromeDriver falha

**Soluções**:
1. Verificar versão do Chrome instalada
2. Atualizar webdriver-manager
3. Revisar logs do workflow

### Problema: Nenhum arquivo gerado

**Soluções**:
1. Verificar logs do scraper
2. Confirmar se site está acessível
3. Testar localmente primeiro

---

## 📝 Boas Práticas

### ✅ Fazer
- ✅ Testar localmente antes de fazer commit
- ✅ Usar execução manual para testar mudanças
- ✅ Manter timeout adequado
- ✅ Verificar artifacts regularmente

### ❌ Evitar
- ❌ Executar muito frequentemente (rate limits)
- ❌ Timeout muito longo (custos)
- ❌ Ignorar falhas consecutivas
- ❌ Commit direto sem testar

---

## 💰 Limites GitHub Actions

### Conta Gratuita
- **2.000 minutos/mês** de execução
- **500 MB** de storage para artifacts

### Estimativa de Uso
- **1 execução diária**: ~15 minutos
- **Total mensal**: ~450 minutos
- **Sobra**: ~1.550 minutos

✅ **Bem dentro do limite!**

---

## 🚀 Próximas Melhorias

### Planejadas
- [ ] Notificações via Telegram/Discord
- [ ] Comparação com resultados anteriores
- [ ] Dashboard de estatísticas
- [ ] Alertas inteligentes
- [ ] Backup automático de dados

---

## 📞 Suporte

### Documentação
- [GitHub Actions](https://docs.github.com/actions)
- [Cron Syntax](https://crontab.guru/)
- [Workflows YAML](https://docs.github.com/actions/reference/workflow-syntax-for-github-actions)

### Ferramentas Úteis
- [Crontab Guru](https://crontab.guru/) - Testar expressões cron
- [YAML Lint](http://www.yamllint.com/) - Validar YAML

---

**Criado em**: 11 de Agosto de 2025  
**Versão**: 1.1.0-rc  
**Status**: ✅ Configurado e Funcionando

