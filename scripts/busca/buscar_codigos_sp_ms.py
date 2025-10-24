#!/usr/bin/env python3
"""
Script para buscar códigos das cidades de SP e MS no site da Caixaimport time
import json
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support.select import Select
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager

URL =https://venda-imoveis.caixa.gov.br/sistema/busca-imovel.asp?sltTipoBusca=imoveis"

# Cidades que queremos buscar
CIDADES_SP = ["BADY BASSITT", "SAO JOSE DO RIO PRETO]CIDADES_MS = ["CAMPO GRANDE", "TRES LAGOAS]

def configurar_driver():
Configura o driver do Chrome"""
    chrome_options = Options()
    chrome_options.add_argument("--headless")
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument(--disable-dev-shm-usage")
    chrome_options.add_argument("--disable-gpu")
    chrome_options.add_argument(--window-size=1920")
    
    service = Service(ChromeDriverManager().install())
    driver = webdriver.Chrome(service=service, options=chrome_options)
    return driver

def buscar_codigos_cidade(driver, estado, cidades):
  Busca códigos das cidades de um estado  print(f"\n🔍 Buscando códigos para {estado}...")
    
    # Acessa o site
    driver.get(URL)
    time.sleep(3   
    # Seleciona o estado
    try:
        estado_select = Select(driver.find_element(By.NAME, "sltEstado))     estado_select.select_by_visible_text(estado)
        print(f✅ Estado {estado} selecionado")
        time.sleep(5)  # Aguarda carregar as cidades
        
        # Busca o select de cidades
        cidade_select = Select(driver.find_element(By.NAME, "sltCidade"))
        
        # Lista todas as cidades disponíveis
        opcoes_cidades = [option.text for option in cidade_select.options]
        print(f📋 Cidades disponíveis em[object Object]estado}: {len(opcoes_cidades)}")
        
        resultados = {}
        
        for cidade_desejada in cidades:
            print(f"\n🔎 Procurando: {cidade_desejada}")
            
            # Busca exata
            cidade_encontrada = None
            codigo_encontrado = None
            
            for option in cidade_select.options:
                if option.text.strip().upper() == cidade_desejada.upper():
                    cidade_encontrada = option.text
                    codigo_encontrado = option.get_attribute("value")
                    break
            
            if cidade_encontrada:
                print(f"✅ Encontrada: [object Object]cidade_encontrada} (código: {codigo_encontrado}))        resultadoscodigo_encontrado] = cidade_encontrada
            else:
                print(f❌ Não encontrada: {cidade_desejada}")
                
                # Busca similar
                cidades_similares =                for option in cidade_select.options:
                    if cidade_desejada.upper() in option.text.upper() or option.text.upper() in cidade_desejada.upper():
                        cidades_similares.append(f"{option.text} (código: {option.get_attribute('value')})")
                
                if cidades_similares:
                    print(f"🔍 Cidades similares encontradas:")
                    for similar in cidades_similares:
                        print(f   • {similar}")
        
        return resultados
        
    except Exception as e:
        print(f"❌ Erro ao buscar cidades de {estado}: {e}")
        return {}

def main():
    "nção principal    print("🏙️ BUSCANDO CÓDIGOS DAS CIDADES DE SP E MS)
    print(=0
    
    driver = configurar_driver()
    
    try:
        # Busca cidades de SP
        codigos_sp = buscar_codigos_cidade(driver, SPADES_SP)
        
        # Busca cidades de MS
        codigos_ms = buscar_codigos_cidade(driver, MSADES_MS)
        
        # Carrega configuração atual
        try:
            with open('configuracao_cidades.json,r, encoding='utf-8') as f:
                config = json.load(f)
        except FileNotFoundError:
            config = {"cidades": {"SC:[object Object]},SP: {}, S": {}}}
        
        # Atualiza com os códigos encontrados
        if codigos_sp:
            config["cidades"]["SP"].update(codigos_sp)
            print(fn✅ Códigos de SP atualizados: {codigos_sp}")
        
        if codigos_ms:
            config["cidades"]["MS"].update(codigos_ms)
            print(fn✅ Códigos de MS atualizados: {codigos_ms}")
        
        # Salva configuração atualizada
        config[data_configuracao]= time.strftime(%Y-%m-%dT%H:%M:%S")
        configobservacao"] = "Códigos de SP e MS obtidos diretamente do site da Caixa     
        with open('configuracao_cidades.json,w, encoding='utf-8') as f:
            json.dump(config, f, indent=2, ensure_ascii=False)
        
        print(fn💾 Configuração salva em configuracao_cidades.json")
        
    finally:
        driver.quit()

if __name__ == "__main__":
    main() 