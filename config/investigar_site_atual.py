#!/usr/bin/env python3
"""
Script para investigar a estrutura atual do site da Caixa
"""

import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager

URL = "https://venda-imoveis.caixa.gov.br/sistema/busca-imovel.asp?sltTipoBusca=imoveis"

def investigar_site():
    """Investiga a estrutura atual do site"""
    chrome_options = Options()
    chrome_options.add_argument("--window-size=1920,1080")
    # chrome_options.add_argument("--headless")  # Comentado para ver o que acontece
    
    service = Service(ChromeDriverManager().install())
    driver = webdriver.Chrome(service=service, options=chrome_options)
    
    try:
        print("🔍 Investigando estrutura do site...")
        print(f"URL: {URL}")
        
        # Acessar página inicial
        driver.get(URL)
        print("✅ Página carregada")
        time.sleep(5)
        
        # Salvar screenshot
        driver.save_screenshot("config/investigacao_site_atual.png")
        print("📸 Screenshot salvo: config/investigacao_site_atual.png")
        
        # Salvar HTML
        with open("config/investigacao_site_atual.html", 'w', encoding='utf-8') as f:
            f.write(driver.page_source)
        print("📄 HTML salvo: config/investigacao_site_atual.html")
        
        # Procurar por elementos de formulário
        print("\n🔍 Procurando elementos de formulário...")
        
        # Procurar por selects
        selects = driver.find_elements(By.TAG_NAME, "select")
        print(f"📋 Encontrados {len(selects)} elementos <select>")
        
        for i, select in enumerate(selects, 1):
            try:
                id_attr = select.get_attribute('id')
                name_attr = select.get_attribute('name')
                class_attr = select.get_attribute('class')
                
                print(f"  Select {i}:")
                print(f"    ID: {id_attr}")
                print(f"    Name: {name_attr}")
                print(f"    Class: {class_attr}")
                
                # Verificar opções
                options = select.find_elements(By.TAG_NAME, "option")
                print(f"    Opções: {len(options)}")
                
                if len(options) <= 10:  # Mostrar apenas se não for muito grande
                    for j, option in enumerate(options[:5], 1):  # Primeiras 5 opções
                        value = option.get_attribute('value')
                        text = option.text.strip()
                        print(f"      {j}. {text} (value: {value})")
                    
                    if len(options) > 5:
                        print(f"      ... e mais {len(options) - 5} opções")
                
                print()
                
            except Exception as e:
                print(f"    ❌ Erro ao analisar select {i}: {e}")
        
        # Procurar por inputs
        inputs = driver.find_elements(By.TAG_NAME, "input")
        print(f"📝 Encontrados {len(inputs)} elementos <input>")
        
        for i, input_elem in enumerate(inputs[:10], 1):  # Primeiros 10 inputs
            try:
                id_attr = input_elem.get_attribute('id')
                name_attr = input_elem.get_attribute('name')
                type_attr = input_elem.get_attribute('type')
                value_attr = input_elem.get_attribute('value')
                
                print(f"  Input {i}:")
                print(f"    ID: {id_attr}")
                print(f"    Name: {name_attr}")
                print(f"    Type: {type_attr}")
                print(f"    Value: {value_attr}")
                print()
                
            except Exception as e:
                print(f"    ❌ Erro ao analisar input {i}: {e}")
        
        # Procurar por botões
        buttons = driver.find_elements(By.TAG_NAME, "button")
        print(f"🔘 Encontrados {len(buttons)} elementos <button>")
        
        for i, button in enumerate(buttons[:5], 1):  # Primeiros 5 botões
            try:
                id_attr = button.get_attribute('id')
                text = button.text.strip()
                onclick = button.get_attribute('onclick')
                
                print(f"  Button {i}:")
                print(f"    ID: {id_attr}")
                print(f"    Text: {text}")
                print(f"    OnClick: {onclick}")
                print()
                
            except Exception as e:
                print(f"    ❌ Erro ao analisar button {i}: {e}")
        
        # Procurar por elementos com IDs específicos
        print("🔍 Procurando elementos com IDs específicos...")
        
        ids_para_procurar = [
            "cmb_estado", "cmb_cidade", "cmb_tipo_imovel", 
            "cmb_faixa_valor", "cmb_quartos", "btn_next0", "btn_next1"
        ]
        
        for id_procurado in ids_para_procurar:
            try:
                elemento = driver.find_element(By.ID, id_procurado)
                print(f"✅ Encontrado elemento com ID: {id_procurado}")
                print(f"   Tag: {elemento.tag_name}")
                print(f"   Class: {elemento.get_attribute('class')}")
            except:
                print(f"❌ Elemento com ID '{id_procurado}' não encontrado")
        
        # Procurar por elementos com classes específicas
        print("\n🔍 Procurando elementos com classes específicas...")
        
        classes_para_procurar = [
            "form-control", "btn", "select", "input", "form-group"
        ]
        
        for classe in classes_para_procurar:
            try:
                elementos = driver.find_elements(By.CLASS_NAME, classe)
                print(f"✅ Encontrados {len(elementos)} elementos com classe: {classe}")
            except:
                print(f"❌ Nenhum elemento com classe '{classe}' encontrado")
        
        print("\n✅ Investigação concluída!")
        
    except Exception as e:
        print(f"❌ Erro durante investigação: {e}")
        
    finally:
        print("Fechando navegador...")
        driver.quit()

if __name__ == "__main__":
    investigar_site() 