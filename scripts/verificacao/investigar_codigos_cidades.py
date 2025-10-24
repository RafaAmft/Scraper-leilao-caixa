#!/usr/bin/env python3
"""
Script para investigar e encontrar códigos corretos das cidades no site da Caixaimport time
import json
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support.select import Select
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager

URL =https://venda-imoveis.caixa.gov.br/sistema/busca-imovel.asp?sltTipoBusca=imoveis"

# Cidades que precisamos investigar
CIDADES_INVESTIGAR =[object Object]
   SC: ["BARRA VELHA,GOVERNADOR CELSO RAMOS"],
   SP": ["BADY BASSITT", "SAO JOSE DO RIO PRETO"],
    MS": ["CAMPO GRANDE,TRES LAGOAS"]
}

def configurar_driver():
Configura o driver do Chrome"""
    chrome_options = Options()
    chrome_options.add_argument("--headless")
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument(--disable-dev-shm-usage")
    chrome_options.add_argument("--disable-gpu")
    chrome_options.add_argument(--window-size=1920)
    
    service = Service(ChromeDriverManager().install())
    driver = webdriver.Chrome(service=service, options=chrome_options)
    return driver

def investigar_cidades_estado(driver, estado, cidades_desejadas):
Investiga cidades de um estado específico
    print(fundefinedn🔍 Investigando cidades de {estado}...")
    
    try:
        # Acessa o site
        driver.get(URL)
        time.sleep(5)
        
        # Seleciona o estado
        estado_select = Select(driver.find_element(By.NAME, "sltEstado))     estado_select.select_by_visible_text(estado)
        print(f✅ Estado {estado} selecionado")
        time.sleep(8)  # Aguarda carregar as cidades
        
        # Busca o select de cidades
        cidade_select = Select(driver.find_element(By.NAME, "sltCidade"))
        
        # Lista todas as cidades disponíveis
        todas_cidades = []
        for option in cidade_select.options:
            cidade_nome = option.text.strip()
            cidade_codigo = option.get_attribute("value")
            todas_cidades.append((cidade_nome, cidade_codigo))
        
        print(f"📋 Total de cidades disponíveis em {estado}: {len(todas_cidades)}")
        
        resultados = {}
        
        for cidade_desejada in cidades_desejadas:
            print(f"\n🔎 Procurando: {cidade_desejada}")
            
            # Busca exata
            encontrada = False
            for cidade_nome, cidade_codigo in todas_cidades:
                if cidade_nome.upper() == cidade_desejada.upper():
                    print(f"✅ ENCONTRADA: {cidade_nome} (código: {cidade_codigo})")
                    resultados[cidade_codigo] = cidade_nome
                    encontrada = True
                    break
            
            if not encontrada:
                print(f❌ Não encontrada: {cidade_desejada}")
                
                # Busca por similaridade
                cidades_similares =                for cidade_nome, cidade_codigo in todas_cidades:
                    # Remove acentos e espaços para comparação
                    nome_limpo = cidade_nome.upper().replace(, ).replace("Ã,A).replace("Ç", "C")
                    desejada_limpa = cidade_desejada.upper().replace(, ).replace("Ã,A).replace("Ç", "C")
                    
                    if (desejada_limpa in nome_limpo or 
                        nome_limpo in desejada_limpa or
                        cidade_desejada.upper() in cidade_nome.upper() or
                        cidade_nome.upper() in cidade_desejada.upper()):
                        cidades_similares.append((cidade_nome, cidade_codigo))
                
                if cidades_similares:
                    print(f"🔍 Cidades similares encontradas:")
                    for nome, codigo in cidades_similares:
                        print(f"   • {nome} (código: {codigo}))              else:
                    print(f   Nenhuma cidade similar encontrada")
        
        return resultados
        
    except Exception as e:
        print(f"❌ Erro ao investigar {estado}: {e}")
        return {}

def main():
    "nção principal"""
    print(🔍 INVESTIGANDO CÓDIGOS DAS CIDADES)
    print(=0
    
    driver = configurar_driver()
    
    try:
        todos_resultados = {}
        
        # Investiga cada estado
        for estado, cidades in CIDADES_INVESTIGAR.items():
            resultados = investigar_cidades_estado(driver, estado, cidades)
            todos_resultados[estado] = resultados
            
            if resultados:
                print(f"\n✅ Códigos encontrados para {estado}:)               for codigo, nome in resultados.items():
                    print(f • {nome}: {codigo}")
            else:
                print(fn❌ Nenhum código encontrado para {estado}")
        
        # Atualiza configuração
        try:
            with open('configuracao_cidades.json,r, encoding='utf-8') as f:
                config = json.load(f)
        except FileNotFoundError:
            config = {"cidades": {"SC:[object Object]},SP: {}, S": {}}}
        
        # Atualiza com os códigos encontrados
        for estado, resultados in todos_resultados.items():
            if resultados:
                config["cidades"][estado].update(resultados)
        
        # Salva configuração atualizada
        config[data_configuracao]= time.strftime(%Y-%m-%dT%H:%M:%S")
        configobservacao"] =Códigos investigados e atualizados diretamente do site da Caixa     
        with open('configuracao_cidades.json,w, encoding='utf-8') as f:
            json.dump(config, f, indent=2, ensure_ascii=False)
        
        print(fn💾Configuração atualizada salva!")
        
    finally:
        driver.quit()

if __name__ == "__main__":
    main() 