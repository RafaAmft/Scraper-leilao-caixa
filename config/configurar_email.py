#!/usr/bin/env python3
"""
Script para configurar email de destino de forma interativa
"""

import json
import os

def configurar_email():
    """Configura o email de destino de forma interativa"""
    
    print("📧 CONFIGURAÇÃO DE EMAIL")
    print("=" * 40)
    print("Este script configura onde os relatórios serão enviados.")
    print("Os relatórios serão salvos localmente e você pode configurar")
    print("um email para receber as notificações.")
    print()
    
    # Verificar se já existe configuração
    config_file = "config/email_config.json"
    if os.path.exists(config_file):
        try:
            with open(config_file, 'r', encoding='utf-8') as f:
                config = json.load(f)
            print(f"📧 Email atual configurado: {config.get('email_destino', 'Nenhum')}")
        except:
            config = {}
    else:
        config = {}
    
    print("\n💡 Opções:")
    print("1. Configurar email de destino")
    print("2. Apenas salvar relatórios localmente (sem email)")
    print("3. Ver configuração atual")
    print("4. Sair")
    
    while True:
        opcao = input("\nEscolha uma opção (1-4): ").strip()
        
        if opcao == "1":
            email = input("Digite seu email de destino: ").strip()
            if "@" in email and "." in email:
                config['email_destino'] = email
                config['enviar_email'] = True
                
                # Salvar configuração
                os.makedirs("config", exist_ok=True)
                with open(config_file, 'w', encoding='utf-8') as f:
                    json.dump(config, f, ensure_ascii=False, indent=2)
                
                print(f"✅ Email configurado: {email}")
                print("📧 Os relatórios serão enviados para este email")
                break
            else:
                print("❌ Email inválido! Digite um email válido.")
        
        elif opcao == "2":
            config['enviar_email'] = False
            config['email_destino'] = None
            
            # Salvar configuração
            os.makedirs("config", exist_ok=True)
            with open(config_file, 'w', encoding='utf-8') as f:
                json.dump(config, f, ensure_ascii=False, indent=2)
            
            print("✅ Configurado para salvar apenas localmente")
            print("📄 Os relatórios serão salvos em arquivos .txt")
            break
        
        elif opcao == "3":
            if os.path.exists(config_file):
                try:
                    with open(config_file, 'r', encoding='utf-8') as f:
                        config = json.load(f)
                    
                    print("\n📧 CONFIGURAÇÃO ATUAL:")
                    print(f"   Email destino: {config.get('email_destino', 'Nenhum')}")
                    print(f"   Enviar email: {config.get('enviar_email', False)}")
                except Exception as e:
                    print(f"❌ Erro ao ler configuração: {e}")
            else:
                print("📧 Nenhuma configuração encontrada")
        
        elif opcao == "4":
            print("👋 Saindo...")
            break
        
        else:
            print("❌ Opção inválida! Digite 1, 2, 3 ou 4.")

def carregar_config_email():
    """Carrega a configuração de email"""
    config_file = "config/email_config.json"
    if os.path.exists(config_file):
        try:
            with open(config_file, 'r', encoding='utf-8') as f:
                return json.load(f)
        except:
            pass
    
    return {
        'email_destino': None,
        'enviar_email': False
    }

if __name__ == "__main__":
    configurar_email() 