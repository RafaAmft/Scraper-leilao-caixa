#!/usr/bin/env python3
"""
Script automático para buscar imóveis em todas as cidades configuradas
"""

import time
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

def carregar_configuracao():
    """Carrega configuração das cidades"""
    try:
        with open('configuracao_cidades.json', 'r', encoding='utf-8') as f:
            return json.load(f)
    except FileNotFoundError:
        print("❌ Arquivo de configuração não encontrado!")
        return None

def carregar_config_gmail():
    """Carrega a configuração do Gmail"""
    script_dir = os.path.dirname(os.path.abspath(__file__))
    config_dir = os.path.join(script_dir, 'config') if not script_dir.endswith('config') else script_dir
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

def gerar_email_temporario():
    """Gera um email temporário"""
    import random
    import string
    
    nome = ''.join(random.choices(string.ascii_lowercase, k=8))
    email = f"{nome}@10minutemail.com"
    return email

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
    try:
        # Criar mensagem
        msg = MIMEMultipart()
        msg['From'] = EMAIL_REMETENTE
        msg['To'] = EMAIL_DESTINATARIO
        msg['Subject'] = f"Relatório de Imóveis - {datetime.now().strftime('%d/%m/%Y')}"
        corpo = f"""
{relatorio}

---
Relatório detalhado anexado.
Gerado automaticamente pelo Scraper Imóveis Caixa
        """
        msg.attach(MIMEText(corpo, 'plain', 'utf-8'))
        relatorio_anexo = MIMEText(relatorio_detalhado, 'plain', 'utf-8')
        relatorio_anexo.add_header('Content-Disposition', 'attachment', filename=f'relatorio_detalhado_{datetime.now().strftime("%Y%m%d_%H%M%S")}.txt')
        msg.attach(relatorio_anexo)
        print(f"📧 Enviando email...")
        print(f"   De: {EMAIL_REMETENTE}")
        print(f"   Para: {EMAIL_DESTINATARIO}")
        server = smtplib.SMTP('smtp.gmail.com', 587)
        server.starttls()
        server.login(EMAIL_REMETENTE, SENHA_APP)
        server.send_message(msg)
        server.quit()
        print("✅ Email enviado com sucesso!")
    except Exception as e:
        print(f"❌ Erro ao enviar email: {e}")
        print("💡 Verifique se o email remetente, destinatário e senha de app estão corretos")
        print("💡 O relatório foi salvo em arquivo local")

def buscar_todas_cidades():
    """Busca imóveis em todas as cidades configuradas"""
    config = carregar_configuracao()
    if not config:
        return
    
    relatorio_completo = []
    total_imoveis = 0
    cidades_processadas = 0
    
    print("🚀 Iniciando busca automática de imóveis...")
    print(f"📅 Data: {datetime.now().strftime('%d/%m/%Y %H:%M')}")
    
    for estado, cidades in config['cidades'].items():
        print(f"\n📍 Processando estado: {estado}")
        
        for codigo, nome in cidades.items():
            cidades_processadas += 1
            print(f"\n🏙️ [{cidades_processadas}] Buscando em {nome}/{estado}...")
            
            # Configurar filtros (ajustar conforme necessário)
            filtros = {
                'estado': estado,
                'codigo_cidade': codigo,
                'nome_cidade': nome,
                'tipo_imovel': '4',  # Indiferente
                'faixa_valor': None,  # Indiferente
                'quartos': None       # Indiferente
            }
            
            try:
                imoveis = buscar_imoveis_com_filtros(filtros)
                
                if imoveis:
                    relatorio_cidade = f"\n🏙️ {nome}/{estado}: {len(imoveis)} imóveis encontrados"
                    
                    # Mostrar os 5 primeiros imóveis
                    for i, imovel in enumerate(imoveis[:5], 1):
                        relatorio_cidade += f"\n  {i}. {imovel['nome_imovel']} - R$ {imovel['valor']}"
                    
                    if len(imoveis) > 5:
                        relatorio_cidade += f"\n  ... e mais {len(imoveis) - 5} imóveis"
                    
                    relatorio_completo.append(relatorio_cidade)
                    total_imoveis += len(imoveis)
                else:
                    relatorio_completo.append(f"\n🏙️ {nome}/{estado}: Nenhum imóvel encontrado")
                
                time.sleep(5)  # Pausa maior entre buscas para evitar erros
                
            except Exception as e:
                relatorio_completo.append(f"\n❌ {nome}/{estado}: Erro - {e}")
                print(f"❌ Erro em {nome}: {e}")
    
    # Contar imóveis por estado
    imoveis_por_estado = {}
    for estado, cidades in config['cidades'].items():
        imoveis_por_estado[estado] = 0
        for codigo, nome in cidades.items():
            # Contar imóveis encontrados para esta cidade
            for relatorio_cidade in relatorio_completo:
                if f"{nome}/{estado}:" in relatorio_cidade:
                    # Extrair número de imóveis do relatório
                    if "imóveis encontrados" in relatorio_cidade:
                        try:
                            num_imoveis = int(relatorio_cidade.split(":")[1].split()[0])
                            imoveis_por_estado[estado] += num_imoveis
                        except:
                            pass
    
    # Gerar relatório resumido (formato solicitado)
    data_atual = datetime.now().strftime("%d/%m/%Y")
    relatorio_resumido = f"Olá, hoje é dia {data_atual}, foram localizados"
    
    # Adicionar contagem por estado
    estados_com_imoveis = []
    for estado, quantidade in imoveis_por_estado.items():
        if quantidade > 0:
            estados_com_imoveis.append(f"{quantidade} imóveis em {estado}")
    
    if estados_com_imoveis:
        relatorio_resumido += " " + ", ".join(estados_com_imoveis) + "."
    else:
        relatorio_resumido += " nenhum imóvel nas cidades monitoradas."
    
    # Relatório detalhado completo
    relatorio_detalhado = f"""
📊 RELATÓRIO DETALHADO DE IMÓVEIS - CAIXA
Data: {datetime.now().strftime('%d/%m/%Y %H:%M')}
Cidades processadas: {cidades_processadas}
Total de imóveis encontrados: {total_imoveis}

{''.join(relatorio_completo)}

---
Relatório gerado automaticamente
    """
    
    # Salvar relatórios em arquivos
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    
    # Salvar relatório resumido
    filename_resumido = f'relatorio_resumido_{timestamp}.txt'
    with open(filename_resumido, 'w', encoding='utf-8') as f:
        f.write(relatorio_resumido)
    
    # Salvar relatório detalhado
    filename_detalhado = f'relatorio_detalhado_{timestamp}.txt'
    with open(filename_detalhado, 'w', encoding='utf-8') as f:
        f.write(relatorio_detalhado)
    
    print(f"\n✅ Relatório resumido salvo em '{filename_resumido}'")
    print(f"✅ Relatório detalhado salvo em '{filename_detalhado}'")
    print(f"📊 Total de imóveis encontrados: {total_imoveis}")
    
    # Mostrar relatório resumido
    print(f"\n📧 RELATÓRIO RESUMIDO:")
    print(f"   {relatorio_resumido}")
    
    # Enviar por email
    print("\n📧 Preparando envio por email...")
    enviar_email_relatorio(relatorio_resumido, relatorio_detalhado)
    
    return relatorio_resumido

if __name__ == "__main__":
    buscar_todas_cidades() 