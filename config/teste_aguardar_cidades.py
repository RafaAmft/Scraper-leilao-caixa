#!/usr/bin/env python3
"""
Script para testar obtenção de cidades aguardando carregamento JavaScript
"""

import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.select import Select
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager

URL = "https://venda-imoveis.caixa.gov.br/sistema/busca-imovel.asp?sltTipoBusca=imoveis"

def testar_aguardar_cidades():
    """Testa aguardando o carregamento das cidades"""
    chrome_options = Options()
    chrome_options.add_argument("--window-size=1920,1080")
    
    service = Service(ChromeDriverManager().install())
    driver = webdriver.Chrome(service=service, options=chrome_options)
    wait = WebDriverWait(driver, 20)  # Aguardar até 20 segundos
    
    try:
        print("🔍 Testando obtenção de cidades aguardando carregamento...")
        
        # Acessar página inicial
        driver.get(URL)
        print("✅ Página carregada")
        time.sleep(5)
        
        # Aguardar elemento do estado estar presente
        select_estado = wait.until(EC.presence_of_element_located((By.ID, "cmb_estado")))
        print("✅ Elemento cmb_estado encontrado")
        
        # Verificar opções do estado
        select = Select(select_estado)
        opcoes_estado = [opt.text for opt in select.options if opt.text.strip()]
        print(f"📋 Estados disponíveis: {len(opcoes_estado)}")
        print(f"   Primeiros 5: {opcoes_estado[:5]}")
        
        # Selecionar SC
        print("📍 Selecionando SC...")
        select.select_by_value("SC")
        
        # Aguardar um pouco para o JavaScript carregar as cidades
        print("⏳ Aguardando carregamento das cidades...")
        time.sleep(5)
        
        # Tentar aguardar até que as cidades sejam carregadas
        try:
            # Aguardar até que o select de cidade tenha opções
            wait.until(lambda driver: len(Select(driver.find_element(By.ID, "cmb_cidade")).options) > 1)
            print("✅ Cidades carregadas!")
        except:
            print("⚠️ Timeout aguardando cidades, tentando de qualquer forma...")
        
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
                
                # Tentar executar JavaScript para forçar carregamento
                print("🔄 Tentando executar JavaScript...")
                driver.execute_script("""
                    // Tentar disparar evento de mudança
                    var selectEstado = document.getElementById('cmb_estado');
                    if (selectEstado) {
                        selectEstado.dispatchEvent(new Event('change'));
                    }
                """)
                time.sleep(3)
                
                # Verificar novamente
                select_cidade_obj = Select(driver.find_element(By.ID, "cmb_cidade"))
                opcoes_cidade = [opt.text for opt in select_cidade_obj.options if opt.text.strip()]
                print(f"🏙️ Cidades após JavaScript: {len(opcoes_cidade)}")
                
                if opcoes_cidade:
                    print("   ✅ Cidades carregadas via JavaScript!")
                    for i, cidade in enumerate(opcoes_cidade[:10], 1):
                        print(f"     {i}. {cidade}")
            
            # Salvar screenshot
            driver.save_screenshot("config/teste_cidades_aguardando.png")
            print("📸 Screenshot salvo: config/teste_cidades_aguardando.png")
            
            # Salvar HTML para análise
            with open("config/teste_cidades_aguardando.html", 'w', encoding='utf-8') as f:
                f.write(driver.page_source)
            print("📄 HTML salvo: config/teste_cidades_aguardando.html")
            
        except Exception as e:
            print(f"❌ Erro ao obter cidades: {e}")
            
    except Exception as e:
        print(f"❌ Erro geral: {e}")
        
    finally:
        print("Fechando navegador...")
        driver.quit()

if __name__ == "__main__":
    testar_aguardar_cidades() 