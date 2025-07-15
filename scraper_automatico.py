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

def enviar_email_relatorio(relatorio):
    """Envia relatório por email"""
    # CONFIGURAR AQUI SUAS INFORMAÇÕES DE EMAIL
    EMAIL_REMETENTE = "seu_email@gmail.com"  # ⚠️ ALTERAR
    EMAIL_DESTINATARIO = "destinatario@email.com"  # ⚠️ ALTERAR
    SENHA_APP = "sua_senha_de_app"  # ⚠️ ALTERAR - Senha de app do Gmail
    
    try:
        # Criar mensagem
        msg = MIMEMultipart()
        msg['From'] = EMAIL_REMETENTE
        msg['To'] = EMAIL_DESTINATARIO
        msg['Subject'] = f"Relatório de Imóveis - {datetime.now().strftime('%d/%m/%Y')}"
        
        # Corpo do email
        corpo = f"""
RELATÓRIO DIÁRIO DE IMÓVEIS - CAIXA
Data: {datetime.now().strftime('%d/%m/%Y %H:%M')}

{relatorio}

---
Gerado automaticamente pelo Scraper Imóveis Caixa
        """
        
        msg.attach(MIMEText(corpo, 'plain', 'utf-8'))
        
        # Enviar email
        server = smtplib.SMTP('smtp.gmail.com', 587)
        server.starttls()
        server.login(EMAIL_REMETENTE, SENHA_APP)
        server.send_message(msg)
        server.quit()
        
        print("✅ Email enviado com sucesso!")
        
    except Exception as e:
        print(f"❌ Erro ao enviar email: {e}")
        print("💡 Dica: Configure as informações de email no script")

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
                
                time.sleep(2)  # Pausa entre buscas
                
            except Exception as e:
                relatorio_completo.append(f"\n❌ {nome}/{estado}: Erro - {e}")
                print(f"❌ Erro em {nome}: {e}")
    
    # Criar relatório final
    relatorio_final = f"""
📊 RELATÓRIO DIÁRIO DE IMÓVEIS - CAIXA
Data: {datetime.now().strftime('%d/%m/%Y %H:%M')}
Cidades processadas: {cidades_processadas}
Total de imóveis encontrados: {total_imoveis}

{''.join(relatorio_completo)}

---
Relatório gerado automaticamente
    """
    
    # Salvar relatório em arquivo
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename_relatorio = f'relatorio_{timestamp}.txt'
    with open(filename_relatorio, 'w', encoding='utf-8') as f:
        f.write(relatorio_final)
    
    print(f"\n✅ Relatório salvo em '{filename_relatorio}'")
    print(f"📊 Total de imóveis encontrados: {total_imoveis}")
    
    # Enviar por email
    print("\n📧 Enviando relatório por email...")
    enviar_email_relatorio(relatorio_final)
    
    return relatorio_final

if __name__ == "__main__":
    buscar_todas_cidades() 