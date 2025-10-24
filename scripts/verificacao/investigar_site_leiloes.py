#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Script para investigar o site de leilões da Caixa e encontrar alternativas
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

def investigar_site_leiloes():
    """Investiga o site de leilões da Caixa"""
    driver = None
    try:
        print("🔍 Investigando o site de leilões da Caixa...")
        driver = setup_driver()
        
        # 1. Acessar página principal da Caixa
        print("\n📡 1. Acessando página principal da Caixa...")
        driver.get("https://www.caixa.gov.br/")
        time.sleep(5)
        
        print(f"Título: {driver.title}")
        print(f"URL: {driver.current_url}")
        
        # 2. Procurar por menu de navegação
        print("\n🔍 2. Procurando menu de navegação...")
        
        # Procurar por menus, navegação, etc.
        nav_selectors = [
            "nav",
            ".menu",
            ".navigation",
            ".navbar",
            "#menu",
            ".main-menu",
            "ul[class*='menu']",
            "ul[class*='nav']"
        ]
        
        for selector in nav_selectors:
            try:
                elements = driver.find_elements(By.CSS_SELECTOR, selector)
                if elements:
                    print(f"✅ Encontrado elemento de navegação: {selector}")
                    for element in elements:
                        print(f"  - Texto: {element.text[:100]}...")
            except:
                pass
        
        # 3. Procurar por todos os links da página
        print("\n🔍 3. Procurando links relacionados a leilões...")
        links = driver.find_elements(By.TAG_NAME, "a")
        
        links_leiloes = []
        links_imoveis = []
        links_gerais = []
        
        for link in links:
            try:
                href = link.get_attribute("href")
                text = link.text.strip().lower()
                
                if not href or not text:
                    continue
                
                # Filtrar links relacionados
                if any(palavra in text for palavra in ["leilão", "leilões", "auction"]):
                    links_leiloes.append({
                        'text': link.text.strip(),
                        'href': href
                    })
                elif any(palavra in text for palavra in ["imóvel", "imóveis", "casa", "apartamento", "terreno"]):
                    links_imoveis.append({
                        'text': link.text.strip(),
                        'href': href
                    })
                elif any(palavra in text for palavra in ["habitação", "moradia", "financiamento"]):
                    links_gerais.append({
                        'text': link.text.strip(),
                        'href': href
                    })
            except:
                pass
        
        print(f"\n📊 Links encontrados:")
        print(f"  - Leilões: {len(links_leiloes)}")
        print(f"  - Imóveis: {len(links_imoveis)}")
        print(f"  - Habitação: {len(links_gerais)}")
        
        # Mostrar links de leilões
        if links_leiloes:
            print(f"\n🎯 Links de Leilões:")
            for i, link in enumerate(links_leiloes[:5], 1):
                print(f"  {i}. {link['text']}: {link['href']}")
        
        # Mostrar links de imóveis
        if links_imoveis:
            print(f"\n🏠 Links de Imóveis:")
            for i, link in enumerate(links_imoveis[:5], 1):
                print(f"  {i}. {link['text']}: {link['href']}")
        
        # 4. Testar URLs alternativas conhecidas
        print(f"\n🔍 4. Testando URLs alternativas...")
        
        urls_alternativas = [
            "https://www.caixa.gov.br/voce/habitacao/",
            "https://www.caixa.gov.br/voce/",
            "https://www.caixa.gov.br/servicos/",
            "https://www.caixa.gov.br/empresas/",
            "https://www.caixa.gov.br/institucional/",
            "https://www.caixa.gov.br/atendimento/",
            "https://www.caixa.gov.br/voce/habitacao/credito-imobiliario/",
            "https://www.caixa.gov.br/voce/habitacao/fgts/",
            "https://www.caixa.gov.br/voce/habitacao/meu-financiamento/",
            "https://www.caixa.gov.br/voce/habitacao/consulta-de-imoveis/"
        ]
        
        urls_validas = []
        
        for url in urls_alternativas:
            print(f"\n📡 Testando: {url}")
            try:
                driver.get(url)
                time.sleep(3)
                
                titulo = driver.title
                url_atual = driver.current_url
                
                print(f"  Título: {titulo}")
                print(f"  URL atual: {url_atual}")
                
                if "não foi encontrada" not in titulo.lower():
                    urls_validas.append({
                        'url': url,
                        'titulo': titulo,
                        'url_atual': url_atual
                    })
                    print(f"  ✅ URL válida!")
                else:
                    print(f"  ❌ Página de erro")
                    
            except Exception as e:
                print(f"  ❌ Erro: {e}")
        
        # 5. Procurar por formulários de busca
        print(f"\n🔍 5. Procurando formulários de busca...")
        forms = driver.find_elements(By.TAG_NAME, "form")
        
        for i, form in enumerate(forms):
            print(f"\nFormulário {i+1}:")
            print(f"  ID: {form.get_attribute('id')}")
            print(f"  Action: {form.get_attribute('action')}")
            print(f"  Method: {form.get_attribute('method')}")
            
            # Procurar por campos de busca
            inputs = form.find_elements(By.TAG_NAME, "input")
            for inp in inputs:
                inp_type = inp.get_attribute("type")
                inp_name = inp.get_attribute("name")
                inp_id = inp.get_attribute("id")
                if inp_type in ["text", "search"] or "busca" in str(inp_name).lower() or "search" in str(inp_id).lower():
                    print(f"    - Campo de busca: type={inp_type}, name={inp_name}, id={inp_id}")
        
        # 6. Verificar se há redirecionamentos
        print(f"\n🔍 6. Verificando redirecionamentos...")
        
        # Testar algumas URLs com redirecionamento
        urls_redirect = [
            "https://www.caixa.gov.br/voce/habitacao/leiloes-de-imoveis",
            "https://www.caixa.gov.br/voce/habitacao/leiloes",
            "https://www.caixa.gov.br/leiloes"
        ]
        
        for url in urls_redirect:
            print(f"\n📡 Testando redirecionamento: {url}")
            try:
                driver.get(url)
                time.sleep(5)  # Aguardar mais tempo para redirecionamento
                
                titulo = driver.title
                url_final = driver.current_url
                
                print(f"  Título final: {titulo}")
                print(f"  URL final: {url_final}")
                
                if url_final != url:
                    print(f"  ✅ Houve redirecionamento!")
                    if "não foi encontrada" not in titulo.lower():
                        urls_validas.append({
                            'url': url,
                            'titulo': titulo,
                            'url_atual': url_final,
                            'redirecionado': True
                        })
                else:
                    print(f"  ❌ Sem redirecionamento")
                    
            except Exception as e:
                print(f"  ❌ Erro: {e}")
        
        # Resultados finais
        print(f"\n🎯 RESULTADOS FINAIS:")
        if urls_validas:
            print(f"✅ Encontradas {len(urls_validas)} URLs válidas:")
            for i, url_info in enumerate(urls_validas, 1):
                print(f"\n{i}. URL original: {url_info['url']}")
                print(f"   Título: {url_info['titulo']}")
                print(f"   URL atual: {url_info['url_atual']}")
                if 'redirecionado' in url_info:
                    print(f"   Redirecionado: Sim")
        else:
            print("❌ Nenhuma URL válida encontrada!")
        
        # Salvar informações para análise
        with open("investigacao_site.txt", "w", encoding="utf-8") as f:
            f.write("INVESTIGAÇÃO DO SITE DE LEILÕES DA CAIXA\n")
            f.write("=" * 50 + "\n\n")
            f.write(f"Data: {time.strftime('%Y-%m-%d %H:%M:%S')}\n")
            f.write(f"URL principal: {driver.current_url}\n")
            f.write(f"Título principal: {driver.title}\n\n")
            
            f.write("LINKS DE LEILÕES:\n")
            for link in links_leiloes:
                f.write(f"- {link['text']}: {link['href']}\n")
            
            f.write("\nLINKS DE IMÓVEIS:\n")
            for link in links_imoveis:
                f.write(f"- {link['text']}: {link['href']}\n")
        
        print(f"\n📄 Relatório salvo em 'investigacao_site.txt'")
        
        # Screenshot final
        driver.save_screenshot("investigacao_site.png")
        print("📸 Screenshot salvo em 'investigacao_site.png'")
        
        # Aguardar input do usuário
        input("\nPressione Enter para fechar o browser...")
        
    except Exception as e:
        print(f"❌ Erro durante investigação: {e}")
        import traceback
        traceback.print_exc()
    
    finally:
        if driver:
            driver.quit()
            print("Browser fechado.")

if __name__ == "__main__":
    investigar_site_leiloes() 