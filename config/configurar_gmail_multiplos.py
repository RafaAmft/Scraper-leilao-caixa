#!/usr/bin/env python3
"""
Script para configurar email Gmail com múltiplos destinatários
"""

import json
import os

def configurar_gmail_multiplos():
    """Configura o email Gmail com múltiplos destinatários"""
    
    print("📧 CONFIGURAÇÃO DO GMAIL - MÚLTIPLOS DESTINATÁRIOS")
    print("=" * 50)
    print("Este script configura o email Gmail para envio de relatórios.")
    print("🔐 Senha de app: (configure a variável de ambiente GMAIL_APP_PASSWORD)")
    print()
    
    # Verificar se já existe configuração
    script_dir = os.path.dirname(os.path.abspath(__file__))
    config_file = os.path.join(script_dir, "gmail_config_multiplos.json")
    
    if os.path.exists(config_file):
        try:
            with open(config_file, 'r', encoding='utf-8') as f:
                config = json.load(f)
            print(f"📧 Email remetente: {config.get('email_remetente', 'Nenhum')}")
            print(f"📧 Destinatários: {len(config.get('email_destinatarios', []))} configurados")
        except:
            config = {'email_destinatarios': []}
    else:
        config = {'email_destinatarios': []}
    
    print("\n💡 Opções:")
    print("1. Configurar email Gmail remetente")
    print("2. Adicionar destinatário")
    print("3. Remover destinatário")
    print("4. Listar destinatários")
    print("5. Testar configuração")
    print("6. Sair")
    
    while True:
        opcao = input("\nEscolha uma opção (1-6): ").strip()
        
        if opcao == "1":
            email = input("Digite seu email Gmail (ex: seuemail@gmail.com): ").strip()
            if "@gmail.com" in email:
                config['email_remetente'] = email
                
                # Salvar configuração
                os.makedirs(script_dir, exist_ok=True)
                with open(config_file, 'w', encoding='utf-8') as f:
                    json.dump(config, f, ensure_ascii=False, indent=2)
                
                print(f"✅ Email Gmail configurado: {email}")
                print("🔐 Senha de app: (configure a variável de ambiente GMAIL_APP_PASSWORD)")
            else:
                print("❌ Email inválido! Deve ser um email Gmail (@gmail.com)")
        
        elif opcao == "2":
            email = input("Digite o email destinatário: ").strip()
            if "@" in email and "." in email:
                if 'email_destinatarios' not in config:
                    config['email_destinatarios'] = []
                
                if email not in config['email_destinatarios']:
                    config['email_destinatarios'].append(email)
                    
                    # Salvar configuração
                    os.makedirs(script_dir, exist_ok=True)
                    with open(config_file, 'w', encoding='utf-8') as f:
                        json.dump(config, f, ensure_ascii=False, indent=2)
                    
                    print(f"✅ Email destinatário adicionado: {email}")
                    print(f"📧 Total de destinatários: {len(config['email_destinatarios'])}")
                else:
                    print(f"⚠️ Email {email} já está na lista de destinatários")
            else:
                print("❌ Email inválido! Digite um email válido.")
        
        elif opcao == "3":
            if not config.get('email_destinatarios'):
                print("❌ Nenhum destinatário configurado!")
                continue
            
            print("\n📧 Destinatários atuais:")
            for i, email in enumerate(config['email_destinatarios'], 1):
                print(f"  {i}. {email}")
            
            try:
                indice = int(input("\nDigite o número do destinatário a remover: ")) - 1
                if 0 <= indice < len(config['email_destinatarios']):
                    email_removido = config['email_destinatarios'].pop(indice)
                    
                    # Salvar configuração
                    with open(config_file, 'w', encoding='utf-8') as f:
                        json.dump(config, f, ensure_ascii=False, indent=2)
                    
                    print(f"✅ Email removido: {email_removido}")
                    print(f"📧 Total de destinatários: {len(config['email_destinatarios'])}")
                else:
                    print("❌ Número inválido!")
            except ValueError:
                print("❌ Digite um número válido!")
        
        elif opcao == "4":
            print("\n📧 CONFIGURAÇÃO ATUAL:")
            print(f"   Email remetente: {config.get('email_remetente', 'Nenhum')}")
            print(f"   Senha de app: (configure a variável de ambiente GMAIL_APP_PASSWORD)")
            
            if config.get('email_destinatarios'):
                print(f"   Destinatários ({len(config['email_destinatarios'])}):")
                for i, email in enumerate(config['email_destinatarios'], 1):
                    print(f"     {i}. {email}")
            else:
                print("   Destinatários: Nenhum configurado")
        
        elif opcao == "5":
            testar_configuracao_gmail_multiplos()
        
        elif opcao == "6":
            print("👋 Saindo...")
            break
        
        else:
            print("❌ Opção inválida! Digite 1, 2, 3, 4, 5 ou 6.")

def testar_configuracao_gmail_multiplos():
    """Testa a configuração do Gmail com múltiplos destinatários"""
    print("\n🧪 TESTE DE CONFIGURAÇÃO GMAIL")
    print("=" * 40)
    
    script_dir = os.path.dirname(os.path.abspath(__file__))
    config_file = os.path.join(script_dir, "gmail_config_multiplos.json")
    
    if not os.path.exists(config_file):
        print("❌ Nenhuma configuração encontrada!")
        print("💡 Configure primeiro o email Gmail")
        return
    
    try:
        with open(config_file, 'r', encoding='utf-8') as f:
            config = json.load(f)
        
        email_remetente = config.get('email_remetente')
        email_destinatarios = config.get('email_destinatarios', [])
        
        if not email_remetente:
            print("❌ Email remetente não configurado!")
            return
        
        if not email_destinatarios:
            print("❌ Nenhum destinatário configurado!")
            return
        
        print(f"📧 Email remetente: {email_remetente}")
        print(f"📧 Destinatários: {len(email_destinatarios)}")
        for i, email in enumerate(email_destinatarios, 1):
            print(f"   {i}. {email}")
        print(f"🔐 Senha de app: (configure a variável de ambiente GMAIL_APP_PASSWORD)")
        
        # Testar conexão SMTP
        print("\n🔍 Testando conexão SMTP...")
        import smtplib
        
        try:
            server = smtplib.SMTP('smtp.gmail.com', 587)
            server.starttls()
            # Substituir a senha fixa por variável de ambiente
            senha_app = os.environ.get("GMAIL_APP_PASSWORD")
            if not senha_app:
                print("❌ A variável de ambiente GMAIL_APP_PASSWORD não está definida.")
                print("💡 Configure a variável de ambiente GMAIL_APP_PASSWORD no seu ambiente.")
                return
            server.login(email_remetente, senha_app)
            server.quit()
            print("✅ Conexão SMTP testada com sucesso!")
            print("✅ Configuração está funcionando!")
        except Exception as e:
            print(f"❌ Erro na conexão SMTP: {e}")
            print("💡 Verifique se o email e senha estão corretos")
    
    except Exception as e:
        print(f"❌ Erro ao testar configuração: {e}")

def carregar_config_gmail_multiplos():
    """Carrega a configuração do Gmail com múltiplos destinatários"""
    script_dir = os.path.dirname(os.path.abspath(__file__))
    config_file = os.path.join(script_dir, "gmail_config_multiplos.json")
    
    if os.path.exists(config_file):
        try:
            with open(config_file, 'r', encoding='utf-8') as f:
                return json.load(f)
        except:
            pass
    
    return {
        'email_remetente': None,
        'email_destinatarios': []
    }

if __name__ == "__main__":
    configurar_gmail_multiplos() 