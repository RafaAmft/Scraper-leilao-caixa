#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Script para testar o endpoint de cidades usando Selenium
"""

import time
import json
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager

def setup_driver_stealth():
    chrome_options = Options()
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")
    chrome_options.add_argument("--disable-blink-features=AutomationControlled")
    chrome_options.add_experimental_option("excludeSwitches", ["enable-automation"])
    chrome_options.add_experimental_option('useAutomationExtension', False)
    chrome_options.add_argument("--user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36")
    chrome_options.add_argument("--window-size=1920,1080")
    chrome_options.add_argument("--start-maximized")
    prefs = {"profile.managed_default_content_settings.images": 2}
    chrome_options.add_experimental_option("prefs", prefs)
    service = Service(ChromeDriverManager().install())
    driver = webdriver.Chrome(service=service, options=chrome_options)
    driver.execute_script("Object.defineProperty(navigator, 'webdriver', {get: () => undefined})")
    return driver

def extrair_cidades(driver, estado):
    print(f"\n📍 Simulando navegação para o estado: {estado}")
    url = "https://venda-imoveis.caixa.gov.br/sistema/busca-imovel.asp?sltTipoBusca=imoveis"
    driver.get(url)
    time.sleep(3)
    try:
        # Selecionar o estado
        select_estado = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.ID, "cmb_estado"))
        )
        select_estado.click()
        option = driver.find_element(By.XPATH, f"//select[@id='cmb_estado']/option[@value='{estado}']")
        option.click()
        print(f"✅ Estado {estado} selecionado")
        time.sleep(3)
        # Aguardar o carregamento das cidades
        select_cidade = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.ID, "cmb_cidade"))
        )
        options = select_cidade.find_elements(By.TAG_NAME, "option")
        cidades = []
        for opt in options:
            value = opt.get_attribute("value")
            text = opt.text.strip()
            if value and value != "":
                cidades.append({"codigo": value, "nome": text})
        print(f"✅ {len(cidades)} cidades encontradas para {estado}")
        # Salvar resultado
        with open(f"cidades_{estado}.json", "w", encoding="utf-8") as f:
            json.dump(cidades, f, ensure_ascii=False, indent=2)
        print(f"💾 Resultado salvo em cidades_{estado}.json")
        # Exibir as 10 primeiras
        for c in cidades[:10]:
            print(f"  {c['codigo']}: {c['nome']}")
    except Exception as e:
        print(f"❌ Erro ao extrair cidades de {estado}: {e}")

def testar_endpoint_selenium():
    print("🔍 Testando endpoint com Selenium (navegação completa)...")
    driver = None
    try:
        driver = setup_driver_stealth()
        estados = ["SC", "MS", "SP"]
        for estado in estados:
            extrair_cidades(driver, estado)
            time.sleep(2)
        input("\nPressione Enter para fechar o browser...")
    except Exception as e:
        print(f"❌ Erro geral: {e}")
        import traceback
        traceback.print_exc()
    finally:
        if driver:
            driver.quit()
            print("Browser fechado.")

if __name__ == "__main__":
    testar_endpoint_selenium() 