"""
Script para verificar os códigos REAIS das cidades do DF no site da Caixa.
"""

import sys
import io
import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager

# Configurar encoding UTF-8 para Windows
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

def verificar_df():
    """Verifica todas as cidades/códigos disponíveis para DF no site da Caixa"""
    print("\n" + "="*70)
    print("VERIFICANDO CODIGOS DO DF NO SITE DA CAIXA")
    print("="*70)
    
    # Configurar Chrome com opções anti-detecção
    chrome_options = Options()
    chrome_options.add_argument("--headless=new")
    chrome_options.add_argument("--window-size=1920,1080")
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")
    chrome_options.add_argument("--disable-blink-features=AutomationControlled")
    chrome_options.add_argument("--disable-gpu")
    chrome_options.add_argument("--disable-extensions")
    chrome_options.add_argument("--disable-popup-blocking")
    chrome_options.add_experimental_option("excludeSwitches", ["enable-automation"])
    chrome_options.add_experimental_option('useAutomationExtension', False)
    chrome_options.add_argument("--user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/140.0.0.0 Safari/537.36")
    
    service = Service(ChromeDriverManager().install())
    driver = webdriver.Chrome(service=service, options=chrome_options)
    
    # Executar script anti-detecção
    driver.execute_script("Object.defineProperty(navigator, 'webdriver', {get: () => undefined})")
    
    try:
        # Acessar página
        url = "https://venda-imoveis.caixa.gov.br/sistema/busca-imovel.asp?sltTipoBusca=imoveis"
        print(f"\nAcessando: {url}")
        driver.get(url)
        time.sleep(5)
        
        # Verificar se caiu no CAPTCHA
        if "radware" in driver.page_source.lower() or "captcha" in driver.page_source.lower():
            print("[AVISO] Site detectou automacao (CAPTCHA). Tentando novamente...")
            driver.quit()
            time.sleep(2)
            # Tentar novamente sem headless
            chrome_options.add_argument("--headless=new")
            driver = webdriver.Chrome(service=service, options=chrome_options)
            driver.execute_script("Object.defineProperty(navigator, 'webdriver', {get: () => undefined})")
            driver.get(url)
            time.sleep(5)
        
        # Verificar se DF está disponível nos estados
        print("\n[1] Verificando se DF esta nos estados disponiveis...")
        select_estado = Select(driver.find_element(By.ID, "cmb_estado"))
        
        estados_disponiveis = []
        for option in select_estado.options:
            valor = option.get_attribute("value")
            texto = option.text.strip()
            if valor:
                estados_disponiveis.append(f"{valor}: {texto}")
                if valor == "DF":
                    print(f"   [OK] DF encontrado: {texto}")
        
        if "DF" not in [e.split(":")[0] for e in estados_disponiveis]:
            print("\n[ERRO] DF NAO ESTA DISPONIVEL no dropdown de estados!")
            print("\nEstados disponiveis:")
            for estado in estados_disponiveis:
                print(f"   > {estado}")
            return None
        
        # Selecionar DF
        print("\n[2] Selecionando DF...")
        select_estado.select_by_value("DF")
        print("   [OK] DF selecionado")
        
        # Aguardar carregamento das cidades
        print("\n[3] Aguardando carregamento das cidades...")
        time.sleep(5)
        
        # Verificar cidades
        select_cidade = Select(driver.find_element(By.ID, "cmb_cidade"))
        
        print(f"\n[4] Verificando cidades disponiveis...")
        cidades_df = {}
        
        for option in select_cidade.options:
            codigo = option.get_attribute("value")
            nome = option.text.strip()
            if codigo and codigo != "":
                cidades_df[codigo] = nome
        
        if not cidades_df:
            print("   [ERRO] NENHUMA cidade encontrada para DF!")
            print(f"   [INFO] Total de opcoes no dropdown: {len(select_cidade.options)}")
            
            # Mostrar todas as opções (incluindo vazias)
            print("\n   Todas as opcoes do dropdown:")
            for i, option in enumerate(select_cidade.options):
                codigo = option.get_attribute("value")
                nome = option.text.strip()
                print(f"      [{i}] value='{codigo}' text='{nome}'")
        else:
            print(f"   [OK] {len(cidades_df)} cidades encontradas!\n")
            print("="*70)
            print("CIDADES DO DF NO SITE DA CAIXA:")
            print("="*70)
            
            for codigo, nome in sorted(cidades_df.items(), key=lambda x: x[1]):
                print(f"   \"{codigo}\": \"{nome}\",")
            
            print("\n" + "="*70)
            
            # Comparar com nossos códigos
            codigos_nossos = {
                "5300108": "BRASILIA",
                "5300100": "DISTRITO FEDERAL",
                "5300109": "BRASILIA - PLANO PILOTO",
                "5300110": "TAGUATINGA",
                "5300111": "CEILANDIA",
                "5300112": "SAMAMBAIA",
                "5300113": "GAMA"
            }
            
            print("\nCOMPARACAO:")
            print("="*70)
            
            # Verificar quais dos nossos códigos existem no site
            print("\nCodigos CORRETOS (existem no site):")
            corretos = []
            for cod, nome in codigos_nossos.items():
                if cod in cidades_df:
                    print(f"   [OK] {cod}: {cidades_df[cod]} (configurado como: {nome})")
                    corretos.append(cod)
            
            print("\nCodigos INCORRETOS (NAO existem no site):")
            incorretos = []
            for cod, nome in codigos_nossos.items():
                if cod not in cidades_df:
                    print(f"   [X] {cod}: {nome}")
                    incorretos.append(cod)
            
            print("\n" + "="*70)
            print(f"RESULTADO: {len(corretos)} corretos, {len(incorretos)} incorretos")
            print("="*70)
        
        return cidades_df
        
    except Exception as e:
        print(f"\n[ERRO]: {e}")
        import traceback
        traceback.print_exc()
        return None
    finally:
        driver.quit()
        print("\nVerificacao concluida!\n")

if __name__ == "__main__":
    verificar_df()

