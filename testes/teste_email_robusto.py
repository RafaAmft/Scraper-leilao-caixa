#!/usr/bin/env python3
"""
Teste robusto de envio de email
"""

import smtplib
import socket
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from datetime import datetime
import json
import os

def carregar_config_gmail():
    """Carrega a configuração do Gmail"""
    script_dir = os.path.dirname(os.path.abspath(__file__))
    config_dir = os.path.join(script_dir, 'config')
    config_file = os.path.join(config_dir, "gmail_config.json")
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

def testar_conectividade():
    """Testa conectividade básica"""
    print("🔍 Testando conectividade...")
    
    # Teste 1: DNS
    try:
        print("📡 Testando resolução DNS...")
        socket.gethostbyname('smtp.gmail.com')
        print("✅ DNS funcionando")
    except socket.gaierror as e:
        print(f"❌ Erro DNS: {e}")
        return False
    
    # Teste 2: Conexão TCP
    try:
        print("🔌 Testando conexão TCP...")
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.settimeout(10)
        sock.connect(('smtp.gmail.com', 587))
        sock.close()
        print("✅ Conexão TCP funcionando")
    except Exception as e:
        print(f"❌ Erro TCP: {e}")
        return False
    
    return True

def testar_smtp_detalhado():
    """Testa SMTP com detalhes"""
    config = carregar_config_gmail()
    EMAIL_REMETENTE = config.get('email_remetente')
    EMAIL_DESTINATARIO = config.get('email_destinatario')
    SENHA_APP = "hfvk igne yago hwou"
    
    if not EMAIL_REMETENTE or not EMAIL_DESTINATARIO:
        print("❌ Configuração de email incompleta!")
        return False
    
    print(f"📧 Email remetente: {EMAIL_REMETENTE}")
    print(f"📧 Email destinatário: {EMAIL_DESTINATARIO}")
    
    try:
        print("🔐 Conectando ao SMTP...")
        server = smtplib.SMTP('smtp.gmail.com', 587, timeout=30)
        print("✅ Conexão SMTP estabelecida")
        
        print("🔒 Iniciando TLS...")
        server.starttls()
        print("✅ TLS ativado")
        
        print("🔑 Fazendo login...")
        server.login(EMAIL_REMETENTE, SENHA_APP)
        print("✅ Login realizado")
        
        # Criar mensagem de teste
        msg = MIMEMultipart()
        msg['From'] = EMAIL_REMETENTE
        msg['To'] = EMAIL_DESTINATARIO
        msg['Subject'] = f"Teste de Email - {datetime.now().strftime('%d/%m/%Y %H:%M')}"
        
        corpo = f"""
Este é um teste de envio de email.

Data/Hora: {datetime.now().strftime('%d/%m/%Y %H:%M:%S')}
Remetente: {EMAIL_REMETENTE}
Destinatário: {EMAIL_DESTINATARIO}

Se você recebeu este email, o sistema está funcionando corretamente.
        """
        
        msg.attach(MIMEText(corpo, 'plain', 'utf-8'))
        
        print("📤 Enviando mensagem...")
        server.send_message(msg)
        print("✅ Mensagem enviada")
        
        server.quit()
        print("✅ Conexão fechada")
        
        return True
        
    except smtplib.SMTPAuthenticationError as e:
        print(f"❌ Erro de autenticação: {e}")
        return False
    except smtplib.SMTPRecipientsRefused as e:
        print(f"❌ Destinatário recusado: {e}")
        return False
    except smtplib.SMTPSenderRefused as e:
        print(f"❌ Remetente recusado: {e}")
        return False
    except smtplib.SMTPDataError as e:
        print(f"❌ Erro de dados: {e}")
        return False
    except smtplib.SMTPConnectError as e:
        print(f"❌ Erro de conexão: {e}")
        return False
    except smtplib.SMTPHeloError as e:
        print(f"❌ Erro HELO: {e}")
        return False
    except smtplib.SMTPNotSupportedError as e:
        print(f"❌ Comando não suportado: {e}")
        return False
    except socket.timeout as e:
        print(f"❌ Timeout: {e}")
        return False
    except socket.gaierror as e:
        print(f"❌ Erro de resolução DNS: {e}")
        return False
    except Exception as e:
        print(f"❌ Erro inesperado: {e}")
        print(f"   Tipo: {type(e).__name__}")
        return False

def main():
    print("🧪 TESTE ROBUSTO DE EMAIL")
    print("=" * 50)
    
    # Teste 1: Conectividade
    if not testar_conectividade():
        print("❌ Problemas de conectividade detectados")
        return
    
    print("\n" + "=" * 50)
    
    # Teste 2: SMTP
    if testar_smtp_detalhado():
        print("\n🎉 TODOS OS TESTES PASSARAM!")
        print("✅ O sistema de email está funcionando corretamente")
    else:
        print("\n❌ FALHA NOS TESTES DE EMAIL")
        print("💡 Verifique a configuração e conectividade")

if __name__ == "__main__":
    main() 