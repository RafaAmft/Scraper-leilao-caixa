#!/usr/bin/env python3
"""
Script para buscar e atualizar os códigos reais das cidades desejadas no site da Caixa
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

# Cidades desejadas
CIDADES_DESEJADAS = {
    'SC': ['JOINVILLE', 'BARRA VELHA', 'BLUMENAU', 'BALNEARIO PICARRAS', 'ITAPEMA', 'SAO FRANCISCO DO SUL', 'GOVERNADOR CELSO RAMOS'],
    'SP': ['BADY BASSITT', 'SAO JOSE DO RIO PRETO', 'ANDRADINA'],
    'MS': ['CAMPO GRANDE', 'TRES LAGOAS']
}

def buscar_cidades_estado(estado):
    """Busca todas as cidades de um estado no site da Caixa"""
    print(f"🔍 Buscando cidades de {estado}...")
    chrome_options = Options()
    chrome_options.add_argument("--headless")
    chrome_options.add_argument("--window-size=1920,1080")
    service = Service(ChromeDriverManager().install())
    driver = webdriver.Chrome(service=service, options=chrome_options)
    try:
        driver.get("https://venda-imoveis.caixa.gov.br/sistema/busca-imovel.asp?sltTipoBusca=imoveis")
        time.sleep(3)
        select_estado = Select(driver.find_element(By.ID, "cmb_estado"))
        select_estado.select_by_value(estado)
        time.sleep(3)
        select_cidade = Select(driver.find_element(By.ID, "cmb_cidade"))
        cidades_estado = {}
        for option in select_cidade.options:
            if option.get_attribute("value") and option.get_attribute("value") != "":
                codigo = option.get_attribute("value")
                nome = option.text.strip()
                cidades_estado[codigo] = nome
        print(f"✅ {len(cidades_estado)} cidades encontradas em {estado}")
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
            # Comparação flexível
            if (cidade_desejada.upper() in nome.upper() or nome.upper() in cidade_desejada.upper()):
                encontradas[codigo] = nome
                print(f"✅ Encontrada: {nome} (código: {codigo})")
                break
        else:
            print(f"❌ Não encontrada: {cidade_desejada}")
    return encontradas

def main():
    print("\n🚀 BUSCANDO CÓDIGOS REAIS DAS CIDADES DESEJADAS...")
    print("="*60)
    cidades_encontradas = {}
    for estado, cidades in CIDADES_DESEJADAS.items():
        print(f"\n📍 {estado}:")
        cidades_estado = buscar_cidades_estado(estado)
        if cidades_estado:
            encontradas = encontrar_cidades_desejadas(cidades_estado, cidades)
            if encontradas:
                cidades_encontradas[estado] = encontradas
        time.sleep(1)
    # Salvar resultado
    if cidades_encontradas:
        config = {
            'data_configuracao': datetime.now().isoformat(),
            'cidades': cidades_encontradas,
            'observacao': 'Códigos verificados automaticamente no site da Caixa'
        }
        with open('configuracao_cidades.json', 'w', encoding='utf-8') as f:
            json.dump(config, f, ensure_ascii=False, indent=2)
        print(f"\n✅ Configuração salva em 'configuracao_cidades.json'")
        print("\n📊 RESULTADO FINAL:")
        for estado, cidades in cidades_encontradas.items():
            print(f"\n{estado}:")
            for codigo, nome in cidades.items():
                print(f"  {codigo}: {nome}")
    else:
        print("❌ Nenhuma cidade desejada foi encontrada!")
    print("\n🎉 Busca concluída!")

if __name__ == "__main__":
    main() 