#!/usr/bin/env python3
"""
Script simples para testar obtenção de cidades
"""

import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.select import Select
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager

URL = "https://venda-imoveis.caixa.gov.br/sistema/busca-imovel.asp?sltTipoBusca=imoveis"

def testar_obtencao_cidades():
    """Testa a obtenção de cidades para SC"""
    chrome_options = Options()
    chrome_options.add_argument("--window-size=1920,1080")
    # chrome_options.add_argument("--headless")  # Comentado para debug
    
    service = Service(ChromeDriverManager().install())
    driver = webdriver.Chrome(service=service, options=chrome_options)
    
    try:
        print("🔍 Testando obtenção de cidades para SC...")
        
        # Acessar página inicial
        driver.get(URL)
        print("✅ Página carregada")
        time.sleep(5)
        
        # Verificar se o elemento existe
        try:
            select_estado = driver.find_element(By.ID, "cmb_estado")
            print("✅ Elemento cmb_estado encontrado")
            
            # Verificar opções do estado
            select = Select(select_estado)
            opcoes_estado = [opt.text for opt in select.options if opt.text.strip()]
            print(f"📋 Estados disponíveis: {len(opcoes_estado)}")
            print(f"   Primeiros 5: {opcoes_estado[:5]}")
            
            # Selecionar SC
            print("📍 Selecionando SC...")
            select.select_by_value("SC")
            time.sleep(3)
            
            # Verificar cidades
            try:
                select_cidade = driver.find_element(By.ID, "cmb_cidade")
                print("✅ Elemento cmb_cidade encontrado")
                
                select_cidade_obj = Select(select_cidade)
                opcoes_cidade = [opt.text for opt in select_cidade_obj.options if opt.text.strip()]
                print(f"🏙️ Cidades disponíveis em SC: {len(opcoes_cidade)}")
                
                if opcoes_cidade:
                    print("   Primeiras 10 cidades:")
                    for i, cidade in enumerate(opcoes_cidade[:10], 1):
                        print(f"     {i}. {cidade}")
                    
                    if len(opcoes_cidade) > 10:
                        print(f"     ... e mais {len(opcoes_cidade) - 10} cidades")
                else:
                    print("   ❌ Nenhuma cidade encontrada")
                
                # Salvar screenshot
                driver.save_screenshot("config/teste_cidades_sc.png")
                print("📸 Screenshot salvo: config/teste_cidades_sc.png")
                
            except Exception as e:
                print(f"❌ Erro ao obter cidades: {e}")
                
        except Exception as e:
            print(f"❌ Erro ao encontrar cmb_estado: {e}")
        
    except Exception as e:
        print(f"❌ Erro geral: {e}")
        
    finally:
        print("Fechando navegador...")
        driver.quit()

if __name__ == "__main__":
    testar_obtencao_cidades() 