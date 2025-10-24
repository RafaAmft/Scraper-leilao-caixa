#!/usr/bin/env python3
"""
Ferramenta para buscar códigos das cidades desejadas no site da Caixa
"""

import time
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.select import Select
from webdriver_manager.chrome import ChromeDriverManager
import json
from datetime import datetime

# Cidades desejadas que precisamos buscar
CIDADES_DESEJADAS = {
    'SC': ['JOINVILLE', 'BARRA VELHA', 'BLUMENAU', 'BALNEARIO PICARRAS', 'ITAJAI', 'GOVERNADOR CELSO RAMOS'],
    'MS': ['CAMPO GRANDE'],
    'SP': ['SAO JOSE DO RIO PRETO', 'BADY BASSIT']
}

def buscar_cidades_estado(estado):
    """Busca todas as cidades de um estado específico"""
    print(f"🔍 Buscando cidades de {estado}...")
    
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
        
        # Extrair todas as cidades
        cidades_estado = {}
        for option in select_cidade.options:
            if option.get_attribute("value") and option.get_attribute("value") != "":
                codigo = option.get_attribute("value")
                nome = option.text.strip()
                cidades_estado[codigo] = nome
        
        print(f"✅ Encontradas {len(cidades_estado)} cidades em {estado}")
        return cidades_estado
        
    except Exception as e:
        print(f"❌ Erro ao buscar cidades de {estado}: {e}")
        return {}
    finally:
        driver.quit()

def encontrar_cidades_desejadas(cidades_estado, cidades_desejadas):
    """Encontra as cidades desejadas na lista de cidades do estado"""
    encontradas = {}
    
    for cidade_desejada in cidades_desejadas:
        for codigo, nome in cidades_estado.items():
            # Comparar nomes (ignorando acentos e maiúsculas)
            if (cidade_desejada.upper() in nome.upper() or 
                nome.upper() in cidade_desejada.upper() or
                cidade_desejada.upper().replace(' ', '') in nome.upper().replace(' ', '') or
                nome.upper().replace(' ', '') in cidade_desejada.upper().replace(' ', '')):
                
                encontradas[codigo] = nome
                print(f"✅ Encontrada: {nome} (código: {codigo})")
                break
        else:
            print(f"❌ Não encontrada: {cidade_desejada}")
    
    return encontradas

def mostrar_todas_cidades_estado(estado, cidades_estado):
    """Mostra todas as cidades de um estado"""
    print(f"\n📋 TODAS AS CIDADES DE {estado}:")
    print("="*50)
    
    # Ordenar por nome
    cidades_ordenadas = sorted(cidades_estado.items(), key=lambda x: x[1])
    
    for i, (codigo, nome) in enumerate(cidades_ordenadas, 1):
        print(f"{i:3d}. {codigo}: {nome}")
    
    print(f"\nTotal: {len(cidades_estado)} cidades")

def main():
    """Função principal"""
    print("="*60)
    print("🔍 FERRAMENTA DE BUSCA DE CÓDIGOS DE CIDADES")
    print("="*60)
    
    cidades_encontradas = {}
    
    for estado, cidades in CIDADES_DESEJADAS.items():
        print(f"\n📍 PROCESSANDO {estado}")
        print("-" * 40)
        
        # Buscar todas as cidades do estado
        cidades_estado = buscar_cidades_estado(estado)
        
        if cidades_estado:
            # Mostrar todas as cidades do estado
            mostrar_todas_cidades_estado(estado, cidades_estado)
            
            # Encontrar cidades desejadas
            print(f"\n🎯 BUSCANDO CIDADES DESEJADAS EM {estado}:")
            print("-" * 40)
            encontradas = encontrar_cidades_desejadas(cidades_estado, cidades)
            
            if encontradas:
                cidades_encontradas[estado] = encontradas
            else:
                print(f"⚠️ Nenhuma cidade desejada encontrada em {estado}")
        
        time.sleep(1)  # Pausa entre estados
    
    # Mostrar resultado final
    print("\n" + "="*60)
    print("📊 RESULTADO FINAL")
    print("="*60)
    
    if cidades_encontradas:
        print("\n✅ CIDADES ENCONTRADAS:")
        for estado, cidades in cidades_encontradas.items():
            print(f"\n📍 {estado}:")
            for codigo, nome in cidades.items():
                print(f"  {codigo}: {nome}")
        
        # Salvar configuração atualizada
        config_atualizada = {
            'data_busca': datetime.now().isoformat(),
            'cidades': cidades_encontradas,
            'observacao': 'Códigos verificados diretamente no site da Caixa'
        }
        
        with open('configuracao_cidades_atualizada.json', 'w', encoding='utf-8') as f:
            json.dump(config_atualizada, f, ensure_ascii=False, indent=2)
        
        print(f"\n✅ Configuração salva em 'configuracao_cidades_atualizada.json'")
        
        # Atualizar arquivo principal
        with open('configuracao_cidades.json', 'w', encoding='utf-8') as f:
            json.dump(config_atualizada, f, ensure_ascii=False, indent=2)
        
        print("✅ Arquivo 'configuracao_cidades.json' atualizado!")
        
    else:
        print("❌ Nenhuma cidade desejada foi encontrada!")
    
    print("\n🎉 Busca concluída!")

if __name__ == "__main__":
    main() 