#!/usr/bin/env python3
"""
Script para verificar e atualizar códigos de cidades do site da Caixa
"""

import time
import json
from datetime import datetime
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.select import Select
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager

URL = "https://venda-imoveis.caixa.gov.br/sistema/busca-imovel.asp?sltTipoBusca=imoveis"

# Estados para verificar (testando apenas alguns primeiro)
ESTADOS_PARA_VERIFICAR = [
    "SC", "SP", "RS"
]

def obter_cidades_do_site(estado):
    """Obtém as cidades disponíveis para um estado no site"""
    chrome_options = Options()
    chrome_options.add_argument("--headless")  # Executar sem interface gráfica
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")
    
    service = Service(ChromeDriverManager().install())
    driver = webdriver.Chrome(service=service, options=chrome_options)
    wait = WebDriverWait(driver, 20)  # Aguardar até 20 segundos
    
    cidades = {}
    
    try:
        print(f"🔍 Verificando cidades de {estado}...")
        
        # Acessar página inicial
        driver.get(URL)
        time.sleep(5)
        
        # Aguardar elemento do estado estar presente
        select_estado = wait.until(EC.presence_of_element_located((By.ID, "cmb_estado")))
        
        # Selecionar estado
        select = Select(select_estado)
        select.select_by_value(estado)
        
        # Aguardar carregamento das cidades
        print(f"  ⏳ Aguardando carregamento das cidades...")
        time.sleep(5)
        
        # Aguardar até que as cidades sejam carregadas
        try:
            wait.until(lambda driver: len(Select(driver.find_element(By.ID, "cmb_cidade")).options) > 1)
        except:
            print(f"  ⚠️ Timeout aguardando cidades para {estado}")
        
        # Obter cidades disponíveis
        select_cidade = Select(driver.find_element(By.ID, "cmb_cidade"))
        
        for option in select_cidade.options:
            if option.get_attribute('value') and option.text.strip():
                codigo = option.get_attribute('value')
                nome = option.text.strip()
                if nome != "Selecione":  # Ignorar opção padrão
                    cidades[codigo] = nome
                    print(f"  ✅ {nome}: {codigo}")
        
    except Exception as e:
        print(f"❌ Erro ao verificar {estado}: {e}")
    
    finally:
        driver.quit()
    
    return cidades

def verificar_codigos_existentes():
    """Verifica os códigos atualmente configurados"""
    print("📋 Verificando códigos existentes...")
    
    # Códigos atuais do scraper principal
    codigos_atuais = {
        "SC": {"8690": "JOINVILLE", "8621": "FLORIANOPOLIS", "8545": "BLUMENAU", "8558": "BRUSQUE", "8598": "CRICIUMA", "8564": "CAMBORIU", "8687": "JARAGUA DO SUL"},
        "SP": {"3550308": "SAO PAULO", "3509502": "CAMPINAS", "3548708": "SANTOS", "3543402": "RIBEIRAO PRETO", "3506607": "BARUERI", "3548500": "SANTO ANDRE"},
        "RS": {"4314902": "PORTO ALEGRE", "4304606": "CAXIAS DO SUL", "4316907": "SANTA MARIA", "4320000": "PELOTAS", "4307005": "GRAVATAI"},
        "PR": {"4106902": "CURITIBA", "4113700": "LONDRINA", "4104808": "CASCAVEL", "4115200": "MARINGA", "4101804": "APUCARANA"},
        "MG": {"3106200": "BELO HORIZONTE", "3170206": "UBERLANDIA", "3149309": "POUSO ALEGRE", "3136702": "JUIZ DE FORA"},
        "RJ": {"3304557": "RIO DE JANEIRO", "3303500": "NOVA IGUACU", "3301702": "DUQUE DE CAXIAS", "3303302": "NITEROI"},
        "BA": {"2927408": "SALVADOR", "2910800": "FEIRA DE SANTANA", "2921005": "ILHEUS", "2929206": "VITORIA DA CONQUISTA"},
        "CE": {"2304400": "FORTALEZA", "2303709": "CAUCAIA", "2307650": "JUAZEIRO DO NORTE", "2312908": "SOBRAL"},
        "PE": {"2611606": "RECIFE", "2609600": "JABOATAO DOS GUARARAPES", "2607901": "PETROPOLIS"},
        "GO": {"5208707": "GOIANIA", "5201405": "ANAPOLIS", "5218806": "RIO VERDE", "5201108": "AGUAS LINDAS DE GOIAS"},
        "MT": {"5103403": "CUIABA", "5102504": "CACERES", "5107602": "RONDONOPOLIS"},
        "MS": {"5002704": "CAMPO GRANDE", "5003207": "CORUMBA", "5004106": "DOURADOS"}
    }
    
    return codigos_atuais

def comparar_codigos(codigos_atuais, codigos_site):
    """Compara códigos atuais com os do site"""
    print("\n🔍 Comparando códigos...")
    
    diferencas = {}
    
    for estado in codigos_site:
        if estado not in diferencas:
            diferencas[estado] = {
                'novos': {},
                'removidos': {},
                'diferentes': {}
            }
        
        # Códigos atuais para este estado
        atuais = codigos_atuais.get(estado, {})
        
        # Códigos do site para este estado
        site = codigos_site[estado]
        
        # Verificar novos códigos
        for codigo, nome in site.items():
            if codigo not in atuais:
                diferencas[estado]['novos'][codigo] = nome
        
        # Verificar códigos removidos
        for codigo, nome in atuais.items():
            if codigo not in site:
                diferencas[estado]['removidos'][codigo] = nome
        
        # Verificar nomes diferentes
        for codigo in set(atuais.keys()) & set(site.keys()):
            if atuais[codigo] != site[codigo]:
                diferencas[estado]['diferentes'][codigo] = {
                    'atual': atuais[codigo],
                    'site': site[codigo]
                }
    
    return diferencas

def salvar_codigos_atualizados(codigos_site):
    """Salva os códigos atualizados"""
    config = {
        'data_atualizacao': datetime.now().isoformat(),
        'total_estados': len(codigos_site),
        'total_cidades': sum(len(cidades) for cidades in codigos_site.values()),
        'cidades': codigos_site
    }
    
    # Salvar arquivo principal
    with open('config/cidades_atualizadas.json', 'w', encoding='utf-8') as f:
        json.dump(config, f, ensure_ascii=False, indent=2)
    
    # Salvar arquivo de configuração para o scraper automático
    config_automatico = {
        'data_configuracao': datetime.now().isoformat(),
        'cidades': codigos_site,
        'observacao': 'Códigos atualizados automaticamente do site da Caixa'
    }
    
    with open('configuracao_cidades.json', 'w', encoding='utf-8') as f:
        json.dump(config_automatico, f, ensure_ascii=False, indent=2)
    
    print("✅ Códigos salvos em 'config/cidades_atualizadas.json'")
    print("✅ Configuração automática atualizada em 'configuracao_cidades.json'")

def gerar_relatorio(diferencas):
    """Gera relatório das diferenças encontradas"""
    print("\n📊 RELATÓRIO DE DIFERENÇAS")
    print("=" * 50)
    
    for estado, diff in diferencas.items():
        if any(diff.values()):  # Se há diferenças
            print(f"\n📍 {estado}:")
            
            if diff['novos']:
                print(f"  ➕ Novos códigos ({len(diff['novos'])}):")
                for codigo, nome in diff['novos'].items():
                    print(f"    {codigo}: {nome}")
            
            if diff['removidos']:
                print(f"  ➖ Códigos removidos ({len(diff['removidos'])}):")
                for codigo, nome in diff['removidos'].items():
                    print(f"    {codigo}: {nome}")
            
            if diff['diferentes']:
                print(f"  🔄 Nomes diferentes ({len(diff['diferentes'])}):")
                for codigo, nomes in diff['diferentes'].items():
                    print(f"    {codigo}: '{nomes['atual']}' → '{nomes['site']}'")

def main():
    """Função principal"""
    print("🚀 INICIANDO ATUALIZAÇÃO DE CÓDIGOS DE CIDADES")
    print("=" * 60)
    print(f"📅 Data: {datetime.now().strftime('%d/%m/%Y %H:%M')}")
    
    # Obter códigos atuais
    codigos_atuais = verificar_codigos_existentes()
    
    # Obter códigos do site
    codigos_site = {}
    for estado in ESTADOS_PARA_VERIFICAR:
        cidades = obter_cidades_do_site(estado)
        if cidades:
            codigos_site[estado] = cidades
        time.sleep(2)  # Pausa maior entre estados
    
    # Comparar códigos
    diferencas = comparar_codigos(codigos_atuais, codigos_site)
    
    # Gerar relatório
    gerar_relatorio(diferencas)
    
    # Salvar códigos atualizados
    salvar_codigos_atualizados(codigos_site)
    
    # Estatísticas finais
    total_cidades = sum(len(cidades) for cidades in codigos_site.values())
    print(f"\n📈 ESTATÍSTICAS FINAIS:")
    print(f"  Estados verificados: {len(codigos_site)}")
    print(f"  Total de cidades: {total_cidades}")
    
    if len(codigos_site) > 0:
        print(f"  Média por estado: {total_cidades / len(codigos_site):.1f}")
    else:
        print("  Média por estado: N/A (nenhum estado processado)")
    
    print("\n✅ Atualização concluída!")

if __name__ == "__main__":
    main() 