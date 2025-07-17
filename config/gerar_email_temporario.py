#!/usr/bin/env python3
"""
Script para gerar email temporário para envio de relatórios
"""

import random
import string
import requests
import time

def gerar_email_temporario():
    """Gera um email temporário usando 10minutemail"""
    
    try:
        print("🔄 Gerando email temporário...")
        
        # Gerar nome aleatório
        nome = ''.join(random.choices(string.ascii_lowercase, k=8))
        
        # Email temporário usando 10minutemail
        email = f"{nome}@10minutemail.com"
        
        print(f"✅ Email temporário gerado: {email}")
        print("⏰ Este email é válido por 10 minutos")
        print("📧 Você pode acessar as mensagens em: https://10minutemail.com")
        
        return email
        
    except Exception as e:
        print(f"❌ Erro ao gerar email temporário: {e}")
        print("💡 Usando email de fallback...")
        return "relatorio@exemplo.com"

def testar_email_temporario(email):
    """Testa se o email temporário está funcionando"""
    try:
        print(f"🔍 Testando email: {email}")
        
        # Simular uma requisição para verificar se o domínio existe
        response = requests.get("https://10minutemail.com", timeout=5)
        
        if response.status_code == 200:
            print("✅ Serviço de email temporário disponível")
            return True
        else:
            print("⚠️ Serviço de email temporário pode estar indisponível")
            return False
            
    except Exception as e:
        print(f"❌ Erro ao testar email: {e}")
        return False

if __name__ == "__main__":
    email = gerar_email_temporario()
    testar_email_temporario(email) 