#!/usr/bin/env python3
"""
Script para verificar se os códigos das cidades configuradas estão corretos
"""

import json
import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support.select import Select
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager

URL = "https://venda-imoveis.caixa.gov.br/sistema/busca-imovel.asp?sltTipoBusca=imoveis"

def carregar_configuracao():
    """Carrega configuração das cidades"""
    try:
        with open('configuracao_cidades.json', 'r', encoding='utf-8') as f:
            return json.load(f)
    except FileNotFoundError:
        print("❌ Arquivo de configuração não encontrado!")
        return None

def verificar_codigo_cidade(estado, codigo, nome_cidade):
    """Verifica se um código de cidade está correto"""
    chrome_options = Options()
    chrome_options.add_argument("--headless")  # Executar sem interface gráfica
    chrome_options.add_argument("--window-size=1920,1080")
    
    service = Service(ChromeDriverManager().install())
    driver = webdriver.Chrome(service=service, options=chrome_options)
    
    try:
        print(f"\n🔍 Verificando {nome_cidade}/{estado} (código: {codigo})...")
        
        # Acessar página inicial
        driver.get(URL)
        time.sleep(3)
        
        # Selecionar estado
        select_estado = Select(driver.find_element(By.ID, "cmb_estado"))
        select_estado.select_by_value(estado)
        time.sleep(5)
        
        # Tentar selecionar cidade
        try:
            select_cidade = Select(driver.find_element(By.ID, "cmb_cidade"))
            select_cidade.select_by_value(codigo)
            time.sleep(2)
            
            # Verificar se a cidade foi selecionada corretamente
            cidade_selecionada = select_cidade.first_selected_option.text
            print(f"   Cidade selecionada: {cidade_selecionada}")
            
            # Verificar se o nome da cidade está correto
            if nome_cidade.upper() in cidade_selecionada.upper():
                print(f"   ✅ CÓDIGO CORRETO para {nome_cidade}")
                return True, cidade_selecionada
            else:
                print(f"   ❌ CÓDIGO INCORRETO - selecionou '{cidade_selecionada}' em vez de '{nome_cidade}'")
                return False, cidade_selecionada
                
        except Exception as e:
            print(f"   ❌ ERRO ao selecionar cidade: {e}")
            return False, None
            
    except Exception as e:
        print(f"   ❌ ERRO geral: {e}")
        return False, None
    finally:
        driver.quit()

def main():
    """Função principal"""
    print("🔍 VERIFICADOR DE CÓDIGOS DE CIDADES")
    print("=" * 50)
    
    config = carregar_configuracao()
    if not config:
        return
    
    resultados = {}
    
    for estado, cidades in config['cidades'].items():
        print(f"\n📍 Verificando estado: {estado}")
        resultados[estado] = {}
        
        for codigo, nome in cidades.items():
            sucesso, cidade_selecionada = verificar_codigo_cidade(estado, codigo, nome)
            resultados[estado][codigo] = {
                'nome': nome,
                'sucesso': sucesso,
                'cidade_selecionada': cidade_selecionada
            }
    
    # Mostrar resumo
    print("\n" + "=" * 50)
    print("📊 RESUMO DA VERIFICAÇÃO")
    print("=" * 50)
    
    for estado, cidades in resultados.items():
        print(f"\n📍 {estado}:")
        for codigo, info in cidades.items():
            status = "✅ CORRETO" if info['sucesso'] else "❌ INCORRETO"
            print(f"   {info['nome']} ({codigo}): {status}")
            if not info['sucesso'] and info['cidade_selecionada']:
                print(f"      Selecionou: {info['cidade_selecionada']}")
    
    # Salvar resultados
    with open('resultados_verificacao_codigos.json', 'w', encoding='utf-8') as f:
        json.dump(resultados, f, indent=2, ensure_ascii=False)
    
    print(f"\n💾 Resultados salvos em: resultados_verificacao_codigos.json")

if __name__ == "__main__":
    main() 