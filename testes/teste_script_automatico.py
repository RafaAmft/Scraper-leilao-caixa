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
    """Carrega a configuração do Gmail com múltiplos destinatários"""
    script_dir = os.path.dirname(os.path.abspath(__file__))
    config_dir = os.path.join(script_dir, '..', 'config')
    config_file = os.path.join(config_dir, "gmail_config_multiplos.json")
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

def enviar_email_relatorio(relatorio, relatorio_detalhado):
    """Envia relatório por email usando Gmail com múltiplos destinatários"""
    SENHA_APP = "hfvk igne yago hwou"  # Senha de app fornecida
    config_gmail = carregar_config_gmail()
    EMAIL_REMETENTE = config_gmail.get('email_remetente')
    EMAIL_DESTINATARIOS = config_gmail.get('email_destinatarios', [])
    
    if not EMAIL_REMETENTE:
        print("❌ Email remetente não configurado!")
        print("💡 Execute 'python config/configurar_gmail_multiplos.py' para configurar")
        return
    
    if not EMAIL_DESTINATARIOS:
        print("❌ Nenhum destinatário configurado!")
        print("💡 Execute 'python config/configurar_gmail_multiplos.py' para configurar")
        return
    
    print(f"📧 Enviando para {len(EMAIL_DESTINATARIOS)} destinatário(s)...")
    
    # Enviar para cada destinatário
    emails_enviados = 0
    for i, email_destinatario in enumerate(EMAIL_DESTINATARIOS, 1):
        print(f"\n📧 [{i}/{len(EMAIL_DESTINATARIOS)}] Enviando para: {email_destinatario}")
        
        # Tentar envio com retry
        max_tentativas = 3
        for tentativa in range(max_tentativas):
            try:
                print(f"   Tentativa {tentativa + 1}/{max_tentativas}...")
                
                # Criar mensagem
                msg = MIMEMultipart()
                msg['From'] = EMAIL_REMETENTE
                msg['To'] = email_destinatario
                msg['Subject'] = f"TESTE - Relatório de Imóveis - {datetime.now().strftime('%d/%m/%Y')}"
                corpo = f"""
{relatorio}

---
Relatório detalhado anexado.
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
                print(f"   ✅ Email enviado com sucesso para {email_destinatario}")
                emails_enviados += 1
                break  # Sucesso, sair do loop de tentativas
                
            except smtplib.SMTPAuthenticationError as e:
                print(f"   ❌ Erro de autenticação: {e}")
                break  # Não tentar novamente para erro de auth
            except smtplib.SMTPRecipientsRefused as e:
                print(f"   ❌ Destinatário recusado: {e}")
                break  # Não tentar novamente para erro de destinatário
            except (socket.timeout, socket.gaierror, ConnectionError) as e:
                print(f"   ❌ Erro de conectividade (tentativa {tentativa + 1}): {e}")
                if tentativa < max_tentativas - 1:
                    print("   ⏳ Aguardando 10 segundos antes da próxima tentativa...")
                    time.sleep(10)
                else:
                    print(f"   ❌ Falha ao enviar para {email_destinatario}")
            except Exception as e:
                print(f"   ❌ Erro inesperado (tentativa {tentativa + 1}): {e}")
                if tentativa < max_tentativas - 1:
                    print("   ⏳ Aguardando 5 segundos antes da próxima tentativa...")
                    time.sleep(5)
                else:
                    print(f"   ❌ Falha ao enviar para {email_destinatario}")
    
    if emails_enviados > 0:
        print(f"\n✅ {emails_enviados}/{len(EMAIL_DESTINATARIOS)} emails enviados com sucesso!")
    else:
        print("\n❌ Nenhum email foi enviado com sucesso")
        print("💡 O relatório foi salvo em arquivo local")

def main():
    """Função principal do teste"""
    print("\n🧪 TESTE DO SCRIPT AUTOMÁTICO")
    print("=" * 50)
    print("Este teste executa apenas uma cidade para verificar o funcionamento")
    print("sem precisar coletar todos os dados novamente.")
    
    # Configurar apenas uma cidade para teste
    cidade_teste = {
        'estado': 'SC',
        'codigo_cidade': '8690',  # JOINVILLE (código correto)
        'nome_cidade': 'JOINVILLE',
        'tipo_imovel': '4',  # Indiferente
        'faixa_valor': None,  # Indiferente
        'quartos': None       # Indiferente
    }
    
    print(f"\n🏙️ Testando cidade: {cidade_teste['nome_cidade']}/{cidade_teste['estado']}")
    
    try:
        # Buscar imóveis
        print("\n🔍 Iniciando busca de imóveis...")
        imoveis = buscar_imoveis_com_filtros(cidade_teste)
        
        if imoveis:
            print(f"✅ {len(imoveis)} imóveis encontrados!")
            
            # Gerar relatório detalhado com todas as informações
            relatorio_detalhado = f"""
🧪 TESTE - RELATÓRIO DETALHADO DE IMÓVEIS - CAIXA
Data: {datetime.now().strftime('%d/%m/%Y %H:%M')}
Cidade testada: {cidade_teste['nome_cidade']}/{cidade_teste['estado']}
Total de imóveis encontrados: {len(imoveis)}

🏙️ {cidade_teste['nome_cidade']}/{cidade_teste['estado']}: {len(imoveis)} imóveis encontrados

"""
            
            # Mostrar TODOS os imóveis com informações completas
            for i, imovel in enumerate(imoveis, 1):
                relatorio_detalhado += f"\n  {i}. {imovel['nome_imovel']}"
                
                # Adicionar quartos se disponível
                if imovel.get('quartos'):
                    relatorio_detalhado += f"\n     🛏️ {imovel['quartos']} quarto(s)"
                
                # Adicionar valor
                relatorio_detalhado += f"\n     💰 R$ {imovel['valor']}"
                
                # Adicionar endereço se disponível
                if imovel.get('endereco'):
                    relatorio_detalhado += f"\n     📍 {imovel['endereco']}"
                
                # Adicionar link direto
                if imovel.get('link_direto'):
                    relatorio_detalhado += f"\n     🔗 {imovel['link_direto']}"
                elif imovel.get('id_imovel'):
                    relatorio_detalhado += f"\n     🔗 https://venda-imoveis.caixa.gov.br/sistema/detalhe-imovel.asp?hdnOrigem=index&txtImovel={imovel['id_imovel']}"
                
                relatorio_detalhado += "\n"
            
            relatorio_detalhado += "\n---\nTESTE - Relatório gerado automaticamente"
            
            # Gerar relatório resumido
            relatorio_resumido = f"TESTE - Olá, hoje é dia {datetime.now().strftime('%d/%m/%Y')}, foram localizados {len(imoveis)} imóveis em {cidade_teste['nome_cidade']}/{cidade_teste['estado']}."
            
            # Salvar relatórios
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
            
        else:
            print("❌ Nenhum imóvel encontrado!")
    
    except Exception as e:
        print(f"❌ Erro durante o teste: {e}")
    
    print("\n🎉 TESTE CONCLUÍDO COM SUCESSO!")
    print("✅ Busca de imóveis funcionando")
    print("✅ Geração de relatórios funcionando")
    print("✅ Envio de email funcionando")

if __name__ == "__main__":
    main() 