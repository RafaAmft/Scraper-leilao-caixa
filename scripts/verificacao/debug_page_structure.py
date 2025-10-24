#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Script de Debug para investigar a estrutura da página do site de leilões
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

def setup_driver():
    """Configura o driver do Chrome com opções de debug"""
    chrome_options = Options()
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")
    chrome_options.add_argument("--disable-gpu")
    chrome_options.add_argument("--window-size=1920,1080")
    # chrome_options.add_argument("--headless")  # Comentado para debug visual
    
    # Adicionar argumentos para debug
    chrome_options.add_argument("--disable-web-security")
    chrome_options.add_argument("--allow-running-insecure-content")
    
    service = Service(ChromeDriverManager().install())
    driver = webdriver.Chrome(service=service, options=chrome_options)
    return driver

def debug_page_structure():
    """Debug da estrutura da página"""
    driver = None
    try:
        print("Iniciando debug da estrutura da página...")
        driver = setup_driver()
        
        # URL do site de leilões
        url = "https://www.caixa.gov.br/voce/habitacao/leiloes-de-imoveis/Paginas/default.aspx"
        print(f"Acessando: {url}")
        
        driver.get(url)
        time.sleep(5)  # Aguardar carregamento
        
        print("\n=== DEBUG DA PÁGINA ===")
        print(f"Título da página: {driver.title}")
        print(f"URL atual: {driver.current_url}")
        
        # Verificar se há redirecionamento
        if "caixa.gov.br" not in driver.current_url:
            print("⚠️  Página foi redirecionada!")
        
        # Salvar HTML da página para análise
        with open("debug_page_source.html", "w", encoding="utf-8") as f:
            f.write(driver.page_source)
        print("✅ HTML da página salvo em 'debug_page_source.html'")
        
        # Procurar por elementos relacionados a estados
        print("\n=== PROCURANDO ELEMENTOS DE ESTADO ===")
        
        # Tentar diferentes seletores para estados
        selectors_to_try = [
            "#cmb_estado",
            "select[name*='estado']",
            "select[id*='estado']",
            "select[class*='estado']",
            ".estado select",
            "#estado",
            "select[data-field='estado']"
        ]
        
        estado_element = None
        for selector in selectors_to_try:
            try:
                elements = driver.find_elements(By.CSS_SELECTOR, selector)
                if elements:
                    print(f"✅ Encontrado elemento com seletor: {selector}")
                    estado_element = elements[0]
                    break
                else:
                    print(f"❌ Nenhum elemento encontrado com: {selector}")
            except Exception as e:
                print(f"❌ Erro ao procurar {selector}: {e}")
        
        if estado_element:
            print(f"\n=== DETALHES DO ELEMENTO ESTADO ===")
            print(f"Tag: {estado_element.tag_name}")
            print(f"ID: {estado_element.get_attribute('id')}")
            print(f"Name: {estado_element.get_attribute('name')}")
            print(f"Class: {estado_element.get_attribute('class')}")
            
            # Listar opções disponíveis
            options = estado_element.find_elements(By.TAG_NAME, "option")
            print(f"\nOpções de estado encontradas ({len(options)}):")
            for i, option in enumerate(options[:10]):  # Mostrar apenas os primeiros 10
                value = option.get_attribute("value")
                text = option.text.strip()
                print(f"  {i+1}. Value: '{value}' | Text: '{text}'")
            
            if len(options) > 10:
                print(f"  ... e mais {len(options) - 10} opções")
        else:
            print("❌ Nenhum elemento de estado encontrado!")
        
        # Procurar por elementos relacionados a cidades
        print("\n=== PROCURANDO ELEMENTOS DE CIDADE ===")
        
        cidade_selectors = [
            "#cmb_cidade",
            "select[name*='cidade']",
            "select[id*='cidade']",
            "select[class*='cidade']",
            ".cidade select",
            "#cidade",
            "select[data-field='cidade']"
        ]
        
        cidade_element = None
        for selector in cidade_selectors:
            try:
                elements = driver.find_elements(By.CSS_SELECTOR, selector)
                if elements:
                    print(f"✅ Encontrado elemento com seletor: {selector}")
                    cidade_element = elements[0]
                    break
                else:
                    print(f"❌ Nenhum elemento encontrado com: {selector}")
            except Exception as e:
                print(f"❌ Erro ao procurar {selector}: {e}")
        
        if cidade_element:
            print(f"\n=== DETALHES DO ELEMENTO CIDADE ===")
            print(f"Tag: {cidade_element.tag_name}")
            print(f"ID: {cidade_element.get_attribute('id')}")
            print(f"Name: {cidade_element.get_attribute('name')}")
            print(f"Class: {cidade_element.get_attribute('class')}")
            print(f"Disabled: {cidade_element.get_attribute('disabled')}")
        else:
            print("❌ Nenhum elemento de cidade encontrado!")
        
        # Procurar por formulários
        print("\n=== PROCURANDO FORMULÁRIOS ===")
        forms = driver.find_elements(By.TAG_NAME, "form")
        print(f"Formulários encontrados: {len(forms)}")
        
        for i, form in enumerate(forms):
            print(f"\nFormulário {i+1}:")
            print(f"  ID: {form.get_attribute('id')}")
            print(f"  Action: {form.get_attribute('action')}")
            print(f"  Method: {form.get_attribute('method')}")
            print(f"  Class: {form.get_attribute('class')}")
        
        # Procurar por botões de busca
        print("\n=== PROCURANDO BOTÕES DE BUSCA ===")
        button_selectors = [
            "button[type='submit']",
            "input[type='submit']",
            "button:contains('Buscar')",
            "button:contains('Pesquisar')",
            "input[value*='Buscar']",
            "input[value*='Pesquisar']",
            ".btn-buscar",
            ".btn-pesquisar",
            "#btnBuscar",
            "#btnPesquisar"
        ]
        
        for selector in button_selectors:
            try:
                elements = driver.find_elements(By.CSS_SELECTOR, selector)
                if elements:
                    print(f"✅ Encontrado botão com seletor: {selector}")
                    for element in elements:
                        print(f"  - Text: '{element.text}' | Value: '{element.get_attribute('value')}'")
                else:
                    print(f"❌ Nenhum botão encontrado com: {selector}")
            except Exception as e:
                print(f"❌ Erro ao procurar {selector}: {e}")
        
        # Verificar se há iframes
        print("\n=== VERIFICANDO IFRAMES ===")
        iframes = driver.find_elements(By.TAG_NAME, "iframe")
        print(f"Iframes encontrados: {len(iframes)}")
        
        for i, iframe in enumerate(iframes):
            print(f"\nIframe {i+1}:")
            print(f"  ID: {iframe.get_attribute('id')}")
            print(f"  Name: {iframe.get_attribute('name')}")
            print(f"  Src: {iframe.get_attribute('src')}")
            print(f"  Class: {iframe.get_attribute('class')}")
        
        # Salvar screenshot para debug visual
        driver.save_screenshot("debug_screenshot.png")
        print("\n✅ Screenshot salvo em 'debug_screenshot.png'")
        
        # Aguardar input do usuário para manter o browser aberto
        input("\nPressione Enter para fechar o browser...")
        
    except Exception as e:
        print(f"❌ Erro durante debug: {e}")
        import traceback
        traceback.print_exc()
    
    finally:
        if driver:
            driver.quit()
            print("Browser fechado.")

if __name__ == "__main__":
    debug_page_structure() 