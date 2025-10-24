#!/usr/bin/env python3
"""
Script para buscar códigos das cidades desejadas e configurar scraper automático
"""

import time
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.select import Select
from webdriver_manager.chrome import ChromeDriverManager
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from datetime import datetime
import json
import os

# Cidades desejadas com seus estados
CIDADES_DESEJADAS = {
    'SC': ['JOINVILLE', 'BARRA VELHA', 'BLUMENAU', 'BALNEARIO PICARRAS', 'ITAJAI', 'GOVERNADOR CELSO RAMOS'],
    'MS': ['CAMPO GRANDE'],
    'SP': ['SAO JOSE DO RIO PRETO', 'BADY BASSIT']
}

def buscar_codigo_cidade(estado, nome_cidade):
    """Busca o código de uma cidade específica no site da Caixa"""
    print(f"🔍 Buscando código para {nome_cidade}/{estado}...")
    
    chrome_options = Options()
    chrome_options.add_argument("--headless")
    chrome_options.add_argument("--window-size=1920,1080")
    
    service = Service(ChromeDriverManager().install())
    driver = webdriver.Chrome(service=service, options=chrome_options)
    
    try:
        # Acessar página inicial
        driver.get("https://venda-imoveis.caixa.gov.br/sistema/busca-imovel.asp?sltTipoBusca=imoveis")
        time.sleep(3)
        
        # Selecionar estado
        select_estado = Select(driver.find_element(By.ID, "cmb_estado"))
        select_estado.select_by_value(estado)
        time.sleep(2)
        
        # Encontrar o select de cidades
        select_cidade = Select(driver.find_element(By.ID, "cmb_cidade"))
        
        # Procurar pela cidade desejada
        for option in select_cidade.options:
            if option.get_attribute("value") and option.get_attribute("value") != "":
                codigo = option.get_attribute("value")
                nome = option.text.strip()
                
                # Comparar nomes (ignorando acentos e maiúsculas)
                if nome_cidade.upper() in nome.upper() or nome.upper() in nome_cidade.upper():
                    print(f"✅ Encontrado: {nome} (código: {codigo})")
                    return codigo, nome
        
        print(f"❌ Cidade {nome_cidade} não encontrada em {estado}")
        return None, None
        
    except Exception as e:
        print(f"❌ Erro ao buscar {nome_cidade}: {e}")
        return None, None
    finally:
        driver.quit()

def buscar_todas_cidades():
    """Busca códigos de todas as cidades desejadas"""
    print("🚀 Iniciando busca de códigos das cidades...")
    
    cidades_encontradas = {}
    
    for estado, cidades in CIDADES_DESEJADAS.items():
        cidades_encontradas[estado] = {}
        
        for cidade in cidades:
            codigo, nome_real = buscar_codigo_cidade(estado, cidade)
            if codigo and nome_real:
                cidades_encontradas[estado][codigo] = nome_real
            time.sleep(1)  # Pausa entre buscas
    
    return cidades_encontradas

def salvar_configuracao(cidades_encontradas):
    """Salva a configuração das cidades encontradas"""
    config = {
        'data_busca': datetime.now().isoformat(),
        'cidades': cidades_encontradas
    }
    
    with open('configuracao_cidades.json', 'w', encoding='utf-8') as f:
        json.dump(config, f, ensure_ascii=False, indent=2)
    
    print("✅ Configuração salva em 'configuracao_cidades.json'")

def criar_script_automatico(cidades_encontradas):
    """Cria script para rodar automaticamente todas as cidades"""
    script_content = '''#!/usr/bin/env python3
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
from src.scraper_caixa.scraper import buscar_imoveis_com_filtros

def carregar_configuracao():
    """Carrega configuração das cidades"""
    with open('configuracao_cidades.json', 'r', encoding='utf-8') as f:
        return json.load(f)

def enviar_email_relatorio(relatorio):
    """Envia relatório por email"""
    # Configurações de email (ajustar conforme necessário)
    EMAIL_REMETENTE = "seu_email@gmail.com"
    EMAIL_DESTINATARIO = "destinatario@email.com"
    SENHA_APP = "sua_senha_de_app"  # Senha de app do Gmail
    
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

def buscar_todas_cidades():
    """Busca imóveis em todas as cidades configuradas"""
    config = carregar_configuracao()
    relatorio_completo = []
    total_imoveis = 0
    
    print("🚀 Iniciando busca automática de imóveis...")
    
    for estado, cidades in config['cidades'].items():
        for codigo, nome in cidades.items():
            print(f"\\n📍 Buscando em {nome}/{estado}...")
            
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
                    relatorio_cidade = f"\\n🏙️ {nome}/{estado}: {len(imoveis)} imóveis encontrados"
                    for i, imovel in enumerate(imoveis[:5], 1):  # Mostrar apenas os 5 primeiros
                        relatorio_cidade += f"\\n  {i}. {imovel['nome_imovel']} - R$ {imovel['valor']}"
                    
                    if len(imoveis) > 5:
                        relatorio_cidade += f"\\n  ... e mais {len(imoveis) - 5} imóveis"
                    
                    relatorio_completo.append(relatorio_cidade)
                    total_imoveis += len(imoveis)
                else:
                    relatorio_completo.append(f"\\n🏙️ {nome}/{estado}: Nenhum imóvel encontrado")
                
                time.sleep(2)  # Pausa entre buscas
                
            except Exception as e:
                relatorio_completo.append(f"\\n❌ {nome}/{estado}: Erro - {e}")
    
    # Criar relatório final
    relatorio_final = f"""
📊 RELATÓRIO DIÁRIO DE IMÓVEIS
Data: {datetime.now().strftime('%d/%m/%Y %H:%M')}
Total de imóveis encontrados: {total_imoveis}

{''.join(relatorio_completo)}
    """
    
    # Salvar relatório em arquivo
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    with open(f'relatorio_{timestamp}.txt', 'w', encoding='utf-8') as f:
        f.write(relatorio_final)
    
    print(f"✅ Relatório salvo em 'relatorio_{timestamp}.txt'")
    
    # Enviar por email
    enviar_email_relatorio(relatorio_final)
    
    return relatorio_final

if __name__ == "__main__":
    buscar_todas_cidades()
'''
    
    with open('scraper_automatico.py', 'w', encoding='utf-8') as f:
        f.write(script_content)
    
    print("✅ Script automático criado: 'scraper_automatico.py'")

def main():
    """Função principal"""
    print("="*60)
    print("🔍 BUSCADOR DE CÓDIGOS DE CIDADES")
    print("="*60)
    
    # Buscar todas as cidades
    cidades_encontradas = buscar_todas_cidades()
    
    # Mostrar resultados
    print("\\n📊 RESULTADOS DA BUSCA:")
    print("="*60)
    
    total_encontradas = 0
    for estado, cidades in cidades_encontradas.items():
        print(f"\\n📍 {estado}:")
        for codigo, nome in cidades.items():
            print(f"  {codigo}: {nome}")
            total_encontradas += 1
    
    print(f"\\n✅ Total de cidades encontradas: {total_encontradas}")
    
    # Salvar configuração
    salvar_configuracao(cidades_encontradas)
    
    # Criar script automático
    criar_script_automatico(cidades_encontradas)
    
    print("\\n🎉 Configuração concluída!")
    print("\\n📋 PRÓXIMOS PASSOS:")
    print("1. Editar 'scraper_automatico.py' e configurar email")
    print("2. Testar o script: python scraper_automatico.py")
    print("3. Configurar agendamento diário (cron/task scheduler)")

if __name__ == "__main__":
    main() 