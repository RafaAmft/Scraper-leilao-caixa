#!/usr/bin/env python3
"""
Teste simples para verificar se o ambiente está funcionando
"""

import sys
import os
import time

# Adicionar o diretório src ao path
sys.path.append('src')

def testar_importacoes():
    """Testa se consegue importar todas as dependências"""
    try:
        import selenium
        print(f"✅ Selenium: {selenium.__version__}")
        
        import pandas as pd
        print(f"✅ Pandas: {pd.__version__}")
        
        import requests
        print(f"✅ Requests: {requests.__version__}")
        
        from bs4 import BeautifulSoup
        print("✅ BeautifulSoup4")
        
        from webdriver_manager.chrome import ChromeDriverManager
        print("✅ WebDriver Manager")
        
        return True
    except Exception as e:
        print(f"❌ Erro ao importar dependências: {e}")
        return False

def testar_chrome_com_webdriver_manager():
    """Testa se consegue abrir o Chrome usando WebDriver Manager"""
    try:
        from selenium import webdriver
        from selenium.webdriver.chrome.options import Options
        from selenium.webdriver.chrome.service import Service
        from webdriver_manager.chrome import ChromeDriverManager
        
        print("\n🔧 Testando Chrome com WebDriver Manager...")
        
        # Configurações básicas
        chrome_options = Options()
        chrome_options.add_argument("--headless")
        chrome_options.add_argument("--no-sandbox")
        chrome_options.add_argument("--disable-dev-shm-usage")
        chrome_options.add_argument("--disable-gpu")
        
        # Forçar uso do WebDriver Manager
        driver_path = ChromeDriverManager().install()
        print(f"🔧 ChromeDriver encontrado em: {driver_path}")
        
        service = Service(driver_path)
        driver = webdriver.Chrome(service=service, options=chrome_options)
        print("✅ Chrome aberto com sucesso!")
        
        # Acessar página simples
        driver.get("https://httpbin.org/status/200")
        print("✅ Acesso à internet funcionando!")
        
        # Verificar título
        titulo = driver.title
        print(f"✅ Título da página: {titulo}")
        
        # Fechar
        driver.quit()
        print("✅ Chrome fechado com sucesso!")
        
        return True
        
    except Exception as e:
        print(f"❌ Erro ao testar Chrome: {e}")
        return False

def testar_modulo_scraper():
    """Testa se consegue importar o módulo do scraper"""
    try:
        from scraper_caixa.scraper import configurar_chromedriver
        print("✅ Módulo scraper importado com sucesso!")
        
        # Testar configuração do driver
        print("🔧 Testando configuração do driver...")
        driver = configurar_chromedriver(headless=True)
        print("✅ Driver configurado com sucesso!")
        
        # Testar acesso a página simples
        driver.get("https://httpbin.org/status/200")
        print("✅ Acesso à internet via módulo funcionando!")
        
        driver.quit()
        print("✅ Driver fechado com sucesso!")
        
        return True
        
    except Exception as e:
        print(f"❌ Erro ao testar módulo scraper: {e}")
        return False

def main():
    """Função principal"""
    print("🧪 TESTE SIMPLES DO AMBIENTE")
    print("=" * 50)
    
    testes = [
        ("Importações básicas", testar_importacoes),
        ("Chrome com WebDriver Manager", testar_chrome_com_webdriver_manager),
        ("Módulo scraper", testar_modulo_scraper)
    ]
    
    resultados = []
    
    for nome_teste, funcao_teste in testes:
        print(f"\n🔍 {nome_teste}...")
        try:
            resultado = funcao_teste()
            resultados.append((nome_teste, resultado))
        except Exception as e:
            print(f"❌ Erro inesperado no teste: {e}")
            resultados.append((nome_teste, False))
    
    print("\n" + "=" * 50)
    print("📊 RESUMO DOS TESTES")
    print("=" * 50)
    
    sucessos = 0
    for nome_teste, resultado in resultados:
        status = "✅ PASSOU" if resultado else "❌ FALHOU"
        print(f"{nome_teste}: {status}")
        if resultado:
            sucessos += 1
    
    print(f"\n🎯 Resultado: {sucessos}/{len(resultados)} testes passaram")
    
    if sucessos == len(resultados):
        print("🎉 Todos os testes passaram! O ambiente está funcionando.")
        print("💡 O problema pode estar no site da Caixa ou na lógica específica.")
    else:
        print("⚠️ Alguns testes falharam. Verifique a configuração do ambiente.")
    
    return sucessos == len(resultados)

if __name__ == "__main__":
    main()
