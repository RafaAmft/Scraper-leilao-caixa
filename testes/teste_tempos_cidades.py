#!/usr/bin/env python3
"""
Script para testar os tempos de carregamento das cidades
"""

import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.select import Select
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager

URL = "https://venda-imoveis.caixa.gov.br/sistema/busca-imovel.asp?sltTipoBusca=imoveis"

def testar_tempos_cidades():
    """Testa os tempos de carregamento das cidades"""
    
    print("🧪 TESTE DE TEMPOS DE CARREGAMENTO")
    print("=" * 50)
    
    chrome_options = Options()
    chrome_options.add_argument("--window-size=1920,1080")
    
    service = Service(ChromeDriverManager().install())
    driver = webdriver.Chrome(service=service, options=chrome_options)
    
    try:
        print("🚀 Acessando página...")
        driver.get(URL)
        time.sleep(3)
        
        # Testar SC
        print("\n📍 Testando SC...")
        select_estado = Select(driver.find_element(By.ID, "cmb_estado"))
        select_estado.select_by_value("SC")
        print("   Estado selecionado, aguardando 5 segundos...")
        time.sleep(5)
        
        # Verificar cidades disponíveis
        select_cidade = Select(driver.find_element(By.ID, "cmb_cidade"))
        cidades_sc = [option.text for option in select_cidade.options]
        print(f"   Cidades disponíveis em SC: {len(cidades_sc)}")
        print(f"   Primeiras 5 cidades: {cidades_sc[:5]}")
        
        # Testar seleção de Joinville
        print("\n🏙️ Testando seleção de Joinville...")
        select_cidade.select_by_value("8690")
        time.sleep(3)
        
        cidade_selecionada = select_cidade.first_selected_option.text
        print(f"   Cidade selecionada: {cidade_selecionada}")
        
        if "JOINVILLE" in cidade_selecionada.upper():
            print("   ✅ Joinville selecionada corretamente!")
        else:
            print(f"   ❌ Erro: selecionou {cidade_selecionada} em vez de Joinville")
        
        # Testar SP
        print("\n📍 Testando SP...")
        select_estado.select_by_value("SP")
        print("   Estado selecionado, aguardando 5 segundos...")
        time.sleep(5)
        
        select_cidade = Select(driver.find_element(By.ID, "cmb_cidade"))
        cidades_sp = [option.text for option in select_cidade.options]
        print(f"   Cidades disponíveis em SP: {len(cidades_sp)}")
        print(f"   Primeiras 5 cidades: {cidades_sp[:5]}")
        
        # Testar seleção de São José do Rio Preto
        print("\n🏙️ Testando seleção de São José do Rio Preto...")
        select_cidade.select_by_value("3549805")
        time.sleep(3)
        
        cidade_selecionada = select_cidade.first_selected_option.text
        print(f"   Cidade selecionada: {cidade_selecionada}")
        
        if "SÃO JOSÉ" in cidade_selecionada.upper() or "SAO JOSE" in cidade_selecionada.upper():
            print("   ✅ São José do Rio Preto selecionada corretamente!")
        else:
            print(f"   ❌ Erro: selecionou {cidade_selecionada} em vez de São José do Rio Preto")
        
        # Testar MS
        print("\n📍 Testando MS...")
        select_estado.select_by_value("MS")
        print("   Estado selecionado, aguardando 5 segundos...")
        time.sleep(5)
        
        select_cidade = Select(driver.find_element(By.ID, "cmb_cidade"))
        cidades_ms = [option.text for option in select_cidade.options]
        print(f"   Cidades disponíveis em MS: {len(cidades_ms)}")
        print(f"   Primeiras 5 cidades: {cidades_ms[:5]}")
        
        # Testar seleção de Campo Grande
        print("\n🏙️ Testando seleção de Campo Grande...")
        select_cidade.select_by_value("5002704")
        time.sleep(3)
        
        cidade_selecionada = select_cidade.first_selected_option.text
        print(f"   Cidade selecionada: {cidade_selecionada}")
        
        if "CAMPO GRANDE" in cidade_selecionada.upper():
            print("   ✅ Campo Grande selecionada corretamente!")
        else:
            print(f"   ❌ Erro: selecionou {cidade_selecionada} em vez de Campo Grande")
        
        print("\n✅ Teste concluído!")
        
    except Exception as e:
        print(f"❌ Erro durante o teste: {e}")
    
    finally:
        driver.quit()

if __name__ == "__main__":
    testar_tempos_cidades() 