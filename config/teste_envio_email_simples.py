#!/usr/bin/env python3
"""
Script para testar o envio de email com Gmail (versão simplificada)
"""

import smtplib
import json
import os
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from datetime import datetime

def carregar_config_gmail():
    """Carrega a configuração do Gmail"""
    # Ajustar caminho baseado na localização do script
    script_dir = os.path.dirname(os.path.abspath(__file__))
    config_file = os.path.join(script_dir, "gmail_config.json")
    
    if os.path.exists(config_file):
        try:
            with open(config_file, 'r', encoding='utf-8') as f:
                return json.load(f)
        except:
            pass
    
    return {
        'email_remetente': None,
        'email_destinatario': None
    }

def testar_envio_email():
    """Testa o envio de email com Gmail"""
    
    print("🧪 TESTE DE ENVIO DE EMAIL")
    print("=" * 40)
    
    # Configurações do Gmail
    SENHA_APP = "hfvk igne yago hwou"
    
    # Carregar configuração do Gmail
    try:
        config_gmail = carregar_config_gmail()
        EMAIL_REMETENTE = config_gmail.get('email_remetente')
        EMAIL_DESTINATARIO = config_gmail.get('email_destinatario')
        
        if not EMAIL_REMETENTE:
            print("❌ Email remetente não configurado!")
            print("💡 Execute 'python config/configurar_gmail.py' para configurar")
            return
        
        if not EMAIL_DESTINATARIO:
            print("❌ Email destinatário não configurado!")
            print("💡 Execute 'python config/configurar_gmail.py' para configurar")
            return
            
    except Exception as e:
        print(f"❌ Erro ao carregar configuração: {e}")
        return
    
    print(f"📧 Email remetente: {EMAIL_REMETENTE}")
    print(f"📧 Email destinatário: {EMAIL_DESTINATARIO}")
    print(f"🔐 Senha de app: {SENHA_APP}")
    
    # Criar mensagem de teste
    msg = MIMEMultipart()
    msg['From'] = EMAIL_REMETENTE
    msg['To'] = EMAIL_DESTINATARIO
    msg['Subject'] = f"Teste de Email - {datetime.now().strftime('%d/%m/%Y %H:%M')}"
    
    # Corpo do email
    corpo = f"""
Olá! Este é um teste de envio de email do Scraper Imóveis Caixa.

Data e hora: {datetime.now().strftime('%d/%m/%Y %H:%M:%S')}

Se você recebeu este email, significa que a configuração está funcionando corretamente!

---
Email de teste gerado automaticamente
    """
    
    msg.attach(MIMEText(corpo, 'plain', 'utf-8'))
    
    # Tentar enviar email
    try:
        print("\n📧 Enviando email de teste...")
        
        server = smtplib.SMTP('smtp.gmail.com', 587)
        server.starttls()
        server.login(EMAIL_REMETENTE, SENHA_APP)
        server.send_message(msg)
        server.quit()
        
        print("✅ Email de teste enviado com sucesso!")
        print(f"📧 Verifique a caixa de entrada de: {EMAIL_DESTINATARIO}")
        
    except Exception as e:
        print(f"❌ Erro ao enviar email: {e}")
        print("💡 Verifique se:")
        print("   - O email remetente está correto")
        print("   - A senha de app está correta")
        print("   - A verificação em duas etapas está ativada no Gmail")

if __name__ == "__main__":
    testar_envio_email() 