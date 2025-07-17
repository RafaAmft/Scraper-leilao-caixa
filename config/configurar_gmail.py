#!/usr/bin/env python3
"""
Script para configurar email Gmail de forma interativa
"""

import json
import os

def configurar_gmail():
    """Configura o email Gmail de forma interativa"""
    
    print("📧 CONFIGURAÇÃO DO GMAIL")
    print("=" * 40)
    print("Este script configura o email Gmail para envio de relatórios.")
    print("A senha de app já está configurada: hfvk igne yago hwou")
    print()
    
    # Verificar se já existe configuração
    # Ajustar caminho baseado na localização do script
    script_dir = os.path.dirname(os.path.abspath(__file__))
    config_file = os.path.join(script_dir, "gmail_config.json")
    if os.path.exists(config_file):
        try:
            with open(config_file, 'r', encoding='utf-8') as f:
                config = json.load(f)
            print(f"📧 Email atual configurado: {config.get('email_remetente', 'Nenhum')}")
            print(f"📧 Destinatário atual: {config.get('email_destinatario', 'Nenhum')}")
        except:
            config = {}
    else:
        config = {}
    
    print("\n💡 Opções:")
    print("1. Configurar email Gmail remetente")
    print("2. Configurar email destinatário")
    print("3. Ver configuração atual")
    print("4. Testar configuração")
    print("5. Sair")
    
    while True:
        opcao = input("\nEscolha uma opção (1-5): ").strip()
        
        if opcao == "1":
            email = input("Digite seu email Gmail (ex: seuemail@gmail.com): ").strip()
            if "@gmail.com" in email:
                config['email_remetente'] = email
                
                # Salvar configuração
                os.makedirs(script_dir, exist_ok=True)
                with open(config_file, 'w', encoding='utf-8') as f:
                    json.dump(config, f, ensure_ascii=False, indent=2)
                
                print(f"✅ Email Gmail configurado: {email}")
                print("🔐 Senha de app: hfvk igne yago hwou")
                break
            else:
                print("❌ Email inválido! Deve ser um email Gmail (@gmail.com)")
        
        elif opcao == "2":
            email = input("Digite o email destinatário: ").strip()
            if "@" in email and "." in email:
                config['email_destinatario'] = email
                
                # Salvar configuração
                os.makedirs(script_dir, exist_ok=True)
                with open(config_file, 'w', encoding='utf-8') as f:
                    json.dump(config, f, ensure_ascii=False, indent=2)
                
                print(f"✅ Email destinatário configurado: {email}")
                break
            else:
                print("❌ Email inválido! Digite um email válido.")
        
        elif opcao == "3":
            if os.path.exists(config_file):
                try:
                    with open(config_file, 'r', encoding='utf-8') as f:
                        config = json.load(f)
                    
                    print("\n📧 CONFIGURAÇÃO ATUAL:")
                    print(f"   Email remetente: {config.get('email_remetente', 'Nenhum')}")
                    print(f"   Email destinatário: {config.get('email_destinatario', 'Nenhum')}")
                    print(f"   Senha de app: hfvk igne yago hwou")
                except Exception as e:
                    print(f"❌ Erro ao ler configuração: {e}")
            else:
                print("📧 Nenhuma configuração encontrada")
        
        elif opcao == "4":
            testar_configuracao_gmail()
        
        elif opcao == "5":
            print("👋 Saindo...")
            break
        
        else:
            print("❌ Opção inválida! Digite 1, 2, 3, 4 ou 5.")

def testar_configuracao_gmail():
    """Testa a configuração do Gmail"""
    print("\n🧪 TESTE DE CONFIGURAÇÃO GMAIL")
    print("=" * 40)
    
    # Ajustar caminho baseado na localização do script
    script_dir = os.path.dirname(os.path.abspath(__file__))
    config_file = os.path.join(script_dir, "gmail_config.json")
    if not os.path.exists(config_file):
        print("❌ Nenhuma configuração encontrada!")
        print("💡 Configure primeiro o email Gmail")
        return
    
    try:
        with open(config_file, 'r', encoding='utf-8') as f:
            config = json.load(f)
        
        email_remetente = config.get('email_remetente')
        email_destinatario = config.get('email_destinatario')
        
        if not email_remetente:
            print("❌ Email remetente não configurado!")
            return
        
        if not email_destinatario:
            print("❌ Email destinatário não configurado!")
            return
        
        print(f"📧 Email remetente: {email_remetente}")
        print(f"📧 Email destinatário: {email_destinatario}")
        print(f"🔐 Senha de app: hfvk igne yago hwou")
        
        # Testar conexão SMTP
        print("\n🔍 Testando conexão SMTP...")
        import smtplib
        
        try:
            server = smtplib.SMTP('smtp.gmail.com', 587)
            server.starttls()
            server.login(email_remetente, "hfvk igne yago hwou")
            server.quit()
            print("✅ Conexão SMTP testada com sucesso!")
            print("✅ Configuração está funcionando!")
        except Exception as e:
            print(f"❌ Erro na conexão SMTP: {e}")
            print("💡 Verifique se o email e senha estão corretos")
    
    except Exception as e:
        print(f"❌ Erro ao testar configuração: {e}")

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

if __name__ == "__main__":
    configurar_gmail() 