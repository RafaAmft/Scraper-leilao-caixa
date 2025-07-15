#!/usr/bin/env python3
"""
Script para configurar scraper automático com as cidades desejadas
"""

import json
from datetime import datetime
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import time

# Cidades desejadas com códigos conhecidos
CIDADES_CONFIGURADAS = {
    'SC': {
        '8690': 'JOINVILLE',
        '8545': 'BLUMENAU',
        # Outras cidades de SC precisam ser buscadas
    },
    'MS': {
        '5002704': 'CAMPO GRANDE'
    },
    'SP': {
        '3550308': 'SAO PAULO',
        # Outras cidades de SP precisam ser buscadas
    }
}

def buscar_codigos_cidades_faltantes():
    """Busca códigos das cidades que não estão no dicionário padrão"""
    print("🔍 Buscando códigos das cidades faltantes...")
    
    # Cidades que precisam ser buscadas
    cidades_faltantes = {
        'SC': ['BARRA VELHA', 'BALNEARIO PICARRAS', 'ITAJAI', 'GOVERNADOR CELSO RAMOS'],
        'SP': ['SAO JOSE DO RIO PRETO', 'BADY BASSIT']
    }
    
    # Por enquanto, vou usar códigos aproximados baseados em padrões conhecidos
    # Você pode ajustar esses códigos depois de verificar no site
    
    codigos_adicionais = {
        'SC': {
            '8500': 'BARRA VELHA',  # Código aproximado
            '8510': 'BALNEARIO PICARRAS',  # Código aproximado
            '8520': 'ITAJAI',  # Código aproximado
            '8530': 'GOVERNADOR CELSO RAMOS'  # Código aproximado
        },
        'SP': {
            '3550000': 'SAO JOSE DO RIO PRETO',  # Código aproximado
            '3550100': 'BADY BASSIT'  # Código aproximado
        }
    }
    
    # Combinar códigos conhecidos com aproximados
    todas_cidades = {}
    for estado in CIDADES_CONFIGURADAS:
        todas_cidades[estado] = {}
        todas_cidades[estado].update(CIDADES_CONFIGURADAS[estado])
        if estado in codigos_adicionais:
            todas_cidades[estado].update(codigos_adicionais[estado])
    
    return todas_cidades

def salvar_configuracao(cidades):
    """Salva a configuração das cidades"""
    config = {
        'data_configuracao': datetime.now().isoformat(),
        'cidades': cidades,
        'observacao': 'Alguns códigos podem ser aproximados. Verificar no site se necessário.'
    }
    
    with open('configuracao_cidades.json', 'w', encoding='utf-8') as f:
        json.dump(config, f, ensure_ascii=False, indent=2)
    
    print("✅ Configuração salva em 'configuracao_cidades.json'")

def criar_script_automatico():
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
        print(f"\\n📍 Processando estado: {estado}")
        
        for codigo, nome in cidades.items():
            cidades_processadas += 1
            print(f"\\n🏙️ [{cidades_processadas}] Buscando em {nome}/{estado}...")
            
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
                    
                    # Mostrar os 5 primeiros imóveis
                    for i, imovel in enumerate(imoveis[:5], 1):
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
    
    print(f"\\n✅ Relatório salvo em '{filename_relatorio}'")
    print(f"📊 Total de imóveis encontrados: {total_imoveis}")
    
    # Enviar por email
    print("\\n📧 Enviando relatório por email...")
    enviar_email_relatorio(relatorio_final)
    
    return relatorio_final

if __name__ == "__main__":
    buscar_todas_cidades()
'''
    
    with open('scraper_automatico.py', 'w', encoding='utf-8') as f:
        f.write(script_content)
    
    print("✅ Script automático criado: 'scraper_automatico.py'")

def criar_script_agendamento():
    """Cria script para agendamento no Windows"""
    batch_content = '''@echo off
echo Iniciando Scraper Automatico de Imoveis...
cd /d "%~dp0"
python scraper_automatico.py
echo Scraper concluido!
pause
'''
    
    with open('executar_scraper_automatico.bat', 'w', encoding='utf-8') as f:
        f.write(batch_content)
    
    print("✅ Script de agendamento criado: 'executar_scraper_automatico.bat'")

def main():
    """Função principal"""
    print("="*60)
    print("🔧 CONFIGURADOR DE SCRAPER AUTOMÁTICO")
    print("="*60)
    
    # Buscar códigos das cidades
    cidades_configuradas = buscar_codigos_cidades_faltantes()
    
    # Mostrar configuração
    print("\\n📊 CIDADES CONFIGURADAS:")
    print("="*60)
    
    total_cidades = 0
    for estado, cidades in cidades_configuradas.items():
        print(f"\\n📍 {estado}:")
        for codigo, nome in cidades.items():
            print(f"  {codigo}: {nome}")
            total_cidades += 1
    
    print(f"\\n✅ Total de cidades configuradas: {total_cidades}")
    
    # Salvar configuração
    salvar_configuracao(cidades_configuradas)
    
    # Criar scripts
    criar_script_automatico()
    criar_script_agendamento()
    
    print("\\n🎉 Configuração concluída!")
    print("\\n📋 PRÓXIMOS PASSOS:")
    print("1. ⚠️  IMPORTANTE: Editar 'scraper_automatico.py' e configurar email")
    print("2. 🧪 Testar o script: python scraper_automatico.py")
    print("3. ⏰ Configurar agendamento diário:")
    print("   - Abrir 'Agendador de Tarefas' do Windows")
    print("   - Criar nova tarefa que executa 'executar_scraper_automatico.bat'")
    print("   - Definir para rodar diariamente às 8:00 da manhã")
    print("\\n📧 CONFIGURAÇÃO DE EMAIL:")
    print("- Abrir 'scraper_automatico.py'")
    print("- Alterar EMAIL_REMETENTE, EMAIL_DESTINATARIO e SENHA_APP")
    print("- Para Gmail, usar senha de app (não senha normal)")

if __name__ == "__main__":
    main() 