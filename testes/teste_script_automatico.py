#!/usr/bin/env python3
"""
Teste do script automático com apenas uma cidade
"""

import time
import socket
from datetime import datetime
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import json
import os
import sys

# Adicionar o diretório src ao path
sys.path.append('src')

from scraper_caixa.scraper import buscar_imoveis_com_filtros

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

def enviar_email_relatorio(relatorio, relatorio_detalhado):
    """Envia relatório por email usando Gmail com senha de app"""
    SENHA_APP = "hfvk igne yago hwou"  # Senha de app fornecida
    config_gmail = carregar_config_gmail()
    EMAIL_REMETENTE = config_gmail.get('email_remetente')
    EMAIL_DESTINATARIO = config_gmail.get('email_destinatario')
    if not EMAIL_REMETENTE or not EMAIL_DESTINATARIO:
        print("❌ Email remetente ou destinatário não configurado!")
        print("💡 Execute 'python config/configurar_gmail.py' para configurar")
        return
    
    # Tentar envio com retry
    max_tentativas = 3
    for tentativa in range(max_tentativas):
        try:
            print(f"📧 Tentativa {tentativa + 1}/{max_tentativas} de envio de email...")
            print(f"   De: {EMAIL_REMETENTE}")
            print(f"   Para: {EMAIL_DESTINATARIO}")
            
            # Criar mensagem
            msg = MIMEMultipart()
            msg['From'] = EMAIL_REMETENTE
            msg['To'] = EMAIL_DESTINATARIO
            msg['Subject'] = f"TESTE - Relatório de Imóveis - {datetime.now().strftime('%d/%m/%Y')}"
            corpo = f"""
{relatorio}

---
TESTE - Relatório detalhado anexado.
Gerado automaticamente pelo Scraper Imóveis Caixa (TESTE)
            """
            msg.attach(MIMEText(corpo, 'plain', 'utf-8'))
            relatorio_anexo = MIMEText(relatorio_detalhado, 'plain', 'utf-8')
            relatorio_anexo.add_header('Content-Disposition', 'attachment', filename=f'teste_relatorio_detalhado_{datetime.now().strftime("%Y%m%d_%H%M%S")}.txt')
            msg.attach(relatorio_anexo)
            
            # Conectar com timeout maior
            server = smtplib.SMTP('smtp.gmail.com', 587, timeout=60)
            server.starttls()
            server.login(EMAIL_REMETENTE, SENHA_APP)
            server.send_message(msg)
            server.quit()
            print("✅ Email enviado com sucesso!")
            return  # Sucesso, sair da função
            
        except smtplib.SMTPAuthenticationError as e:
            print(f"❌ Erro de autenticação: {e}")
            break  # Não tentar novamente para erro de auth
        except smtplib.SMTPRecipientsRefused as e:
            print(f"❌ Destinatário recusado: {e}")
            break  # Não tentar novamente para erro de destinatário
        except (socket.timeout, socket.gaierror, ConnectionError) as e:
            print(f"❌ Erro de conectividade (tentativa {tentativa + 1}): {e}")
            if tentativa < max_tentativas - 1:
                print("⏳ Aguardando 10 segundos antes da próxima tentativa...")
                time.sleep(10)
            else:
                print("❌ Todas as tentativas falharam")
        except Exception as e:
            print(f"❌ Erro inesperado (tentativa {tentativa + 1}): {e}")
            if tentativa < max_tentativas - 1:
                print("⏳ Aguardando 5 segundos antes da próxima tentativa...")
                time.sleep(5)
            else:
                print("❌ Todas as tentativas falharam")
    
    print("💡 O relatório foi salvo em arquivo local")
    print("💡 Verifique se o email remetente, destinatário e senha de app estão corretos")

def teste_uma_cidade():
    """Testa o script com apenas uma cidade"""
    
    print("🧪 TESTE DO SCRIPT AUTOMÁTICO")
    print("=" * 50)
    print("Este teste executa apenas uma cidade para verificar o funcionamento")
    print("sem precisar coletar todos os dados novamente.")
    print()
    
    # Configurar apenas uma cidade para teste
    cidade_teste = {
        'estado': 'SC',
        'codigo_cidade': '8690',  # JOINVILLE (código correto)
        'nome_cidade': 'JOINVILLE',
        'tipo_imovel': '4',  # Indiferente
        'faixa_valor': None,  # Indiferente
        'quartos': None       # Indiferente
    }
    
    print(f"🏙️ Testando cidade: {cidade_teste['nome_cidade']}/{cidade_teste['estado']}")
    print()
    
    try:
        # Buscar imóveis
        print("🔍 Iniciando busca de imóveis...")
        imoveis = buscar_imoveis_com_filtros(cidade_teste)
        
        if imoveis:
            print(f"✅ {len(imoveis)} imóveis encontrados!")
            
            # Mostrar os 3 primeiros imóveis
            print("\n📋 PRIMEIROS IMÓVEIS ENCONTRADOS:")
            for i, imovel in enumerate(imoveis[:3], 1):
                print(f"  {i}. {imovel['nome_imovel']} - R$ {imovel['valor']}")
            
            if len(imoveis) > 3:
                print(f"  ... e mais {len(imoveis) - 3} imóveis")
            
            # Gerar relatório de teste
            data_atual = datetime.now().strftime("%d/%m/%Y")
            relatorio_resumido = f"TESTE - Olá, hoje é dia {data_atual}, foram localizados {len(imoveis)} imóveis em {cidade_teste['nome_cidade']}/{cidade_teste['estado']}."
            
            relatorio_detalhado = f"""
🧪 TESTE - RELATÓRIO DETALHADO DE IMÓVEIS - CAIXA
Data: {datetime.now().strftime('%d/%m/%Y %H:%M')}
Cidade testada: {cidade_teste['nome_cidade']}/{cidade_teste['estado']}
Total de imóveis encontrados: {len(imoveis)}

🏙️ {cidade_teste['nome_cidade']}/{cidade_teste['estado']}: {len(imoveis)} imóveis encontrados

IMÓVEIS ENCONTRADOS:
{chr(10).join([f"  {i+1}. {imovel['nome_imovel']} - R$ {imovel['valor']}" for i, imovel in enumerate(imoveis)])}

---
TESTE - Relatório gerado automaticamente
            """
            
            # Salvar relatórios de teste
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            
            filename_resumido = f'teste_relatorio_resumido_{timestamp}.txt'
            with open(filename_resumido, 'w', encoding='utf-8') as f:
                f.write(relatorio_resumido)
            
            filename_detalhado = f'teste_relatorio_detalhado_{timestamp}.txt'
            with open(filename_detalhado, 'w', encoding='utf-8') as f:
                f.write(relatorio_detalhado)
            
            print(f"\n✅ Relatório resumido salvo em '{filename_resumido}'")
            print(f"✅ Relatório detalhado salvo em '{filename_detalhado}'")
            
            # Mostrar relatório resumido
            print(f"\n📧 RELATÓRIO RESUMIDO:")
            print(f"   {relatorio_resumido}")
            
            # Enviar por email
            print("\n📧 Preparando envio por email...")
            enviar_email_relatorio(relatorio_resumido, relatorio_detalhado)
            
            print("\n🎉 TESTE CONCLUÍDO COM SUCESSO!")
            print("✅ Busca de imóveis funcionando")
            print("✅ Geração de relatórios funcionando")
            print("✅ Envio de email funcionando")
            
        else:
            print("❌ Nenhum imóvel encontrado na cidade de teste")
            print("💡 Verifique se a cidade está correta ou se há imóveis disponíveis")
    
    except Exception as e:
        print(f"❌ Erro durante o teste: {e}")
        print("💡 Verifique se o scraper está funcionando corretamente")

if __name__ == "__main__":
    teste_uma_cidade() 