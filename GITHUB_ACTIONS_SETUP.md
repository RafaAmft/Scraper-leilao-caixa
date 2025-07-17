# 🚀 GitHub Actions - Configuração e Uso

Este documento explica como configurar e usar os GitHub Actions para automatizar o scraper de imóveis da Caixa.

## 📋 Workflows Disponíveis

### 1. 🏠 **Scraper Diário** (`scraper-daily.yml`)
- **Execução automática**: Todos os dias às 8h da manhã (horário de Brasília)
- **Execução manual**: Via interface do GitHub
- **Função**: Executa o scraper completo e envia relatórios por email

### 2. 🧪 **Teste do Scraper** (`test-scraper.yml`)
- **Execução automática**: Em pull requests
- **Execução manual**: Via interface do GitHub
- **Função**: Testa o scraper com uma cidade e valida o funcionamento

## ⚙️ Configuração Inicial

### 1. **Configurar Secrets do GitHub**

Acesse seu repositório no GitHub:
1. Vá para **Settings** → **Secrets and variables** → **Actions**
2. Clique em **New repository secret**
3. Adicione os seguintes secrets:

#### **EMAIL_REMETENTE**
```
d4rk.funer4l@gmail.com
```

#### **EMAIL_DESTINATARIOS**
```
rafael.a.fontes@hotmail.com,felipe.ms.nsn@gmail.com,vjfontes20@gmail.com
```

#### **SENHA_APP**
```
hfvk igne yago hwou
```

### 2. **Verificar Configuração**

Após configurar os secrets, os workflows estarão disponíveis em:
- **Actions** → **🏠 Scraper Imóveis Caixa - Execução Diária**
- **Actions** → **🧪 Teste do Scraper**

## 🎮 Como Usar

### **Execução Automática**
- O scraper diário executa automaticamente às 8h da manhã
- Os relatórios são enviados por email para todos os destinatários configurados
- Os resultados ficam disponíveis como artifacts por 7 dias

### **Execução Manual**

#### **Scraper Completo:**
1. Vá para **Actions** → **🏠 Scraper Imóveis Caixa - Execução Diária**
2. Clique em **Run workflow**
3. Selecione a branch (main)
4. Opcional: Marque "Modo teste" para executar apenas uma cidade
5. Clique em **Run workflow**

#### **Teste do Scraper:**
1. Vá para **Actions** → **🧪 Teste do Scraper**
2. Clique em **Run workflow**
3. Selecione a branch (main)
4. Opcional: Especifique uma cidade para teste
5. Clique em **Run workflow**

## 📊 Monitoramento

### **Verificar Execuções:**
- Acesse **Actions** no seu repositório
- Clique no workflow desejado
- Veja o histórico de execuções

### **Logs e Debug:**
- Clique em uma execução específica
- Veja os logs de cada step
- Em caso de erro, os logs mostram detalhes do problema

### **Artifacts (Resultados):**
- Após cada execução, os arquivos gerados ficam disponíveis como artifacts
- Clique em **relatorios-XXXX** para baixar os resultados
- Inclui: relatórios, dados JSON/CSV, screenshots

## 🔧 Personalização

### **Alterar Horário de Execução**
Edite o arquivo `.github/workflows/scraper-daily.yml`:
```yaml
schedule:
  - cron: '0 11 * * *'  # 11h UTC = 8h BRT
```

### **Adicionar Novos Destinatários**
1. Vá para **Settings** → **Secrets and variables** → **Actions**
2. Edite o secret **EMAIL_DESTINATARIOS**
3. Adicione novos emails separados por vírgula

### **Modificar Cidades Monitoradas**
Edite o arquivo `configuracao_cidades.json` no repositório.

## 🚨 Troubleshooting

### **Erro de Autenticação de Email**
- Verifique se o secret **SENHA_APP** está correto
- Confirme se o email remetente tem autenticação de 2 fatores ativada
- Verifique se a senha de app está correta

### **Erro de Chrome/Selenium**
- O workflow instala automaticamente o Chrome
- Se houver problemas, verifique os logs do step "Instalar Chrome"

### **Nenhum Imóvel Encontrado**
- Verifique se o site da Caixa está funcionando
- Confirme se os códigos das cidades estão corretos
- Veja os screenshots gerados para debug

### **Workflow Não Executa**
- Verifique se os arquivos estão na branch `main`
- Confirme se os secrets estão configurados
- Verifique se o repositório tem permissões para Actions

## 📈 Benefícios

### **✅ Automação Completa**
- Execução diária sem intervenção manual
- Relatórios enviados automaticamente
- Backup dos resultados no GitHub

### **✅ Monitoramento**
- Logs detalhados de cada execução
- Notificações de sucesso/falha
- Histórico de execuções

### **✅ Flexibilidade**
- Execução manual quando necessário
- Modo teste para validação rápida
- Configuração fácil via interface

### **✅ Confiabilidade**
- Execução em ambiente controlado
- Verificação automática de erros
- Artifacts para análise posterior

## 🔗 Links Úteis

- [GitHub Actions Documentation](https://docs.github.com/en/actions)
- [Cron Syntax](https://crontab.guru/)
- [GitHub Secrets](https://docs.github.com/en/actions/security-guides/encrypted-secrets)

---

**💡 Dica**: Após a primeira execução bem-sucedida, você receberá relatórios diários automaticamente no email configurado! 