#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Script para encontrar a URL correta do site de leilões da Caixa
"""

import time
import requests
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager

def setup_driver():
    """Configura o driver do Chrome"""
    chrome_options = Options()
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")
    chrome_options.add_argument("--disable-gpu")
    chrome_options.add_argument("--window-size=1920,1080")
    
    service = Service(ChromeDriverManager().install())
    driver = webdriver.Chrome(service=service, options=chrome_options)
    return driver

def encontrar_url_leiloes():
    """Encontra a URL correta do site de leilões"""
    driver = None
    try:
        print("🔍 Procurando a URL correta do site de leilões da Caixa...")
        driver = setup_driver()
        
        # URLs para testar
        urls_para_testar = [
            "https://www.caixa.gov.br/voce/habitacao/leiloes-de-imoveis/",
            "https://www.caixa.gov.br/voce/habitacao/leiloes-de-imoveis",
            "https://www.caixa.gov.br/voce/habitacao/leiloes/",
            "https://www.caixa.gov.br/voce/habitacao/leiloes",
            "https://www.caixa.gov.br/voce/leiloes/",
            "https://www.caixa.gov.br/voce/leiloes",
            "https://www.caixa.gov.br/leiloes/",
            "https://www.caixa.gov.br/leiloes",
            "https://www.caixa.gov.br/voce/habitacao/",
            "https://www.caixa.gov.br/voce/habitacao"
        ]
        
        urls_validas = []
        
        for url in urls_para_testar:
            print(f"\n📡 Testando: {url}")
            try:
                driver.get(url)
                time.sleep(3)
                
                titulo = driver.title
                url_atual = driver.current_url
                
                print(f"  Título: {titulo}")
                print(f"  URL atual: {url_atual}")
                
                # Verificar se não é página de erro
                if "não foi encontrada" not in titulo.lower() and "not found" not in titulo.lower():
                    if "leilão" in titulo.lower() or "leilões" in titulo.lower() or "imóveis" in titulo.lower():
                        print(f"  ✅ POSSÍVEL URL VÁLIDA!")
                        urls_validas.append({
                            'url': url,
                            'titulo': titulo,
                            'url_atual': url_atual
                        })
                    else:
                        print(f"  ⚠️  Página carregou, mas não parece ser de leilões")
                else:
                    print(f"  ❌ Página de erro")
                    
            except Exception as e:
                print(f"  ❌ Erro ao acessar: {e}")
        
        # Testar também a página principal da Caixa
        print(f"\n📡 Testando página principal da Caixa...")
        try:
            driver.get("https://www.caixa.gov.br/")
            time.sleep(3)
            
            # Procurar links relacionados a leilões
            links = driver.find_elements(By.TAG_NAME, "a")
            links_leiloes = []
            
            for link in links:
                href = link.get_attribute("href")
                text = link.text.lower()
                
                if href and ("leilão" in text or "leilões" in text or "imóveis" in text):
                    links_leiloes.append({
                        'text': link.text,
                        'href': href
                    })
            
            if links_leiloes:
                print(f"  ✅ Encontrados {len(links_leiloes)} links relacionados a leilões:")
                for link in links_leiloes:
                    print(f"    - {link['text']}: {link['href']}")
                    
                    # Testar o link
                    try:
                        driver.get(link['href'])
                        time.sleep(3)
                        titulo = driver.title
                        url_atual = driver.current_url
                        
                        if "não foi encontrada" not in titulo.lower():
                            urls_validas.append({
                                'url': link['href'],
                                'titulo': titulo,
                                'url_atual': url_atual,
                                'fonte': 'link da página principal'
                            })
                    except:
                        pass
        
        except Exception as e:
            print(f"  ❌ Erro ao acessar página principal: {e}")
        
        # Resultados
        print(f"\n🎯 RESULTADOS:")
        if urls_validas:
            print(f"✅ Encontradas {len(urls_validas)} URLs válidas:")
            for i, url_info in enumerate(urls_validas, 1):
                print(f"\n{i}. URL: {url_info['url']}")
                print(f"   Título: {url_info['titulo']}")
                print(f"   URL atual: {url_info['url_atual']}")
                if 'fonte' in url_info:
                    print(f"   Fonte: {url_info['fonte']}")
        else:
            print("❌ Nenhuma URL válida encontrada!")
            
            # Salvar screenshot da página atual para análise
            driver.save_screenshot("pagina_atual.png")
            print("📸 Screenshot salvo em 'pagina_atual.png' para análise")
        
        # Aguardar input do usuário
        input("\nPressione Enter para fechar o browser...")
        
    except Exception as e:
        print(f"❌ Erro durante busca: {e}")
        import traceback
        traceback.print_exc()
    
    finally:
        if driver:
            driver.quit()
            print("Browser fechado.")

if __name__ == "__main__":
    encontrar_url_leiloes() 