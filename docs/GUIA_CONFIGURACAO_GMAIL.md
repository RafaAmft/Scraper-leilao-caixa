# 📧 GUIA DE CONFIGURAÇÃO DO GMAIL

## 🔧 **CONFIGURAÇÃO INICIAL**

### **1. Configurar Email Gmail**
Execute o script de configuração:
```bash
python config/configurar_gmail.py
```

### **2. Opções Disponíveis**
- **Opção 1**: Configurar email Gmail remetente
- **Opção 2**: Configurar email destinatário  
- **Opção 3**: Ver configuração atual
- **Opção 4**: Testar configuração
- **Opção 5**: Sair

### **3. Configuração Automática**
- Email remetente: Seu email Gmail (@gmail.com)
- Email destinatário: Email onde receber os relatórios
- Senha de app: `hfvk igne yago hwou` (já configurada)

## 🧪 **TESTE DE CONFIGURAÇÃO**

### **1. Testar Conexão**
```bash
python config/teste_envio_email.py
```

### **2. O que o teste faz**
- Verifica se os emails estão configurados
- Testa a conexão SMTP com Gmail
- Envia um email de teste
- Confirma se tudo está funcionando

## 📧 **FORMATO DOS RELATÓRIOS**

### **Corpo do Email**
```
Olá, hoje é dia 16/07/2025, foram localizados 5 imóveis em SC, 12 imóveis em SP, 1 imóveis em MS.

---
Relatório detalhado anexado.
Gerado automaticamente pelo Scraper Imóveis Caixa
```

### **Anexo**
- Arquivo `.txt` com relatório detalhado
- Nome: `relatorio_detalhado_YYYYMMDD_HHMMSS.txt`

## 🚀 **COMO USAR**

### **1. Configurar (uma vez)**
```bash
python config/configurar_gmail.py
```

### **2. Testar (opcional)**
```bash
python config/teste_envio_email.py
```

### **3. Executar Scraper**
```bash
python scraper_automatico.py
```

## ⚠️ **REQUISITOS DO GMAIL**

### **Verificação em Duas Etapas**
- Deve estar ativada na conta Gmail
- Acesse: https://myaccount.google.com/security

### **Senha de App**
- Já configurada: `hfvk igne yago hwou`
- Não precisa memorizar
- Permite acesso total à conta

### **Configurações de Segurança**
- Aplicativos menos seguros: **NÃO** precisa ativar
- Senha de app é mais segura

## 🔍 **TROUBLESHOOTING**

### **Erro: "Username and Password not accepted"**
- Verifique se o email remetente está correto
- Confirme se a verificação em duas etapas está ativada
- Verifique se a senha de app está correta

### **Erro: "SMTP Authentication failed"**
- Gere uma nova senha de app
- Acesse: https://myaccount.google.com/apppasswords

### **Email não chega**
- Verifique a pasta de spam
- Confirme se o email destinatário está correto
- Teste com o script de teste primeiro

## 📁 **ARQUIVOS DE CONFIGURAÇÃO**

### **config/gmail_config.json**
```json
{
  "email_remetente": "seuemail@gmail.com",
  "email_destinatario": "destinatario@email.com"
}
```

### **Arquivos de Relatório**
- `relatorio_resumido_YYYYMMDD_HHMMSS.txt`
- `relatorio_detalhado_YYYYMMDD_HHMMSS.txt`

## 🎯 **EXEMPLO DE USO COMPLETO**

```bash
# 1. Configurar Gmail
python config/configurar_gmail.py

# 2. Testar configuração
python config/teste_envio_email.py

# 3. Executar scraper automático
python scraper_automatico.py
```

## 📞 **SUPORTE**

Se encontrar problemas:
1. Execute o teste de configuração
2. Verifique os requisitos do Gmail
3. Confirme se os emails estão corretos
4. Teste com email de teste primeiro

---

**Configuração Segura e Funcional!** ✅ 