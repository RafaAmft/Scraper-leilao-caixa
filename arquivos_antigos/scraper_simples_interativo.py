import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait, Select
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
import pandas as pd
from datetime import datetime
import re

URL = "https://venda-imoveis.caixa.gov.br/sistema/busca-imovel.asp?sltTipoBusca=imoveis"

# Dicionário com cidades e seus códigos
CIDADES_SC = {
    "8690": "JOINVILLE",
    "8621": "FLORIANOPOLIS", 
    "8545": "BLUMENAU",
    "8558": "BRUSQUE",
    "8598": "CRICIUMA",
    "8564": "CAMBORIU",
    "8687": "JARAGUA DO SUL"
}

CIDADES_SP = {
    "3550308": "SAO PAULO",
    "3509502": "CAMPINAS",
    "3548708": "SANTOS",
    "3543402": "RIBEIRAO PRETO"
}

CIDADES_RS = {
    "4314902": "PORTO ALEGRE",
    "4304606": "CAXIAS DO SUL",
    "4316907": "SANTA MARIA",
    "4320000": "PELOTAS"
}

CIDADES_PR = {
    "4106902": "CURITIBA",
    "4113700": "LONDRINA",
    "4104808": "CASCAVEL",
    "4115200": "MARINGA"
}

def obter_codigo_cidade(estado, entrada_usuario):
    """Converte nome da cidade em código ou retorna o código se já for um código"""
    if estado == "SC":
        cidades = CIDADES_SC
    elif estado == "SP":
        cidades = CIDADES_SP
    elif estado == "RS":
        cidades = CIDADES_RS
    elif estado == "PR":
        cidades = CIDADES_PR
    else:
        return entrada_usuario
    
    # Se a entrada já é um código, retorna ela
    if entrada_usuario in cidades:
        return entrada_usuario
    
    # Se é um nome de cidade, procura o código
    entrada_upper = entrada_usuario.upper()
    for codigo, nome in cidades.items():
        if entrada_upper in nome.upper() or nome.upper() in entrada_upper:
            return codigo
    
    # Se não encontrou, retorna a entrada original
    return entrada_usuario

def main():
    print("="*60)
    print("🏠 SCRAPER INTERATIVO - IMÓVEIS CAIXA")
    print("="*60)
    
    print("\n📍 ESTADOS DISPONÍVEIS:")
    print("1. SC (Santa Catarina)")
    print("2. SP (São Paulo)")
    print("3. RS (Rio Grande do Sul)")
    print("4. PR (Paraná)")
    
    print("\n🏠 TIPOS DE IMÓVEL:")
    print("1. Casa")
    print("2. Apartamento")
    print("4. Indiferente")
    
    print("\n💰 FAIXAS DE VALOR:")
    print("1. Até R$ 50.000")
    print("2. R$ 50.000 a R$ 100.000")
    print("3. R$ 100.000 a R$ 150.000")
    print("4. R$ 150.000 a R$ 200.000")
    print("5. R$ 200.000 a R$ 300.000")
    print("6. R$ 300.000 a R$ 500.000")
    print("7. Acima de R$ 500.000")
    
    print("\n🛏️ QUARTOS:")
    print("1. 1 quarto")
    print("2. 2 quartos")
    print("3. 3 quartos")
    print("4. 4+ quartos")
    
    print("\n" + "="*60)
    print("🔧 CONFIGURAÇÃO DOS FILTROS")
    print("="*60)
    
    # Obter estado
    print("\n📍 DIGITE O ESTADO (SC, SP, RS, PR):")
    estado = input(">>> ").upper().strip()
    
    # Obter cidade
    print(f"\n🏙️ DIGITE O CÓDIGO OU NOME DA CIDADE:")
    if estado == "SC":
        print("Cidades disponíveis em SC:")
        for codigo, nome in CIDADES_SC.items():
            print(f"{codigo} - {nome}")
    elif estado == "SP":
        print("Cidades disponíveis em SP:")
        for codigo, nome in CIDADES_SP.items():
            print(f"{codigo} - {nome}")
    elif estado == "RS":
        print("Cidades disponíveis em RS:")
        for codigo, nome in CIDADES_RS.items():
            print(f"{codigo} - {nome}")
    elif estado == "PR":
        print("Cidades disponíveis em PR:")
        for codigo, nome in CIDADES_PR.items():
            print(f"{codigo} - {nome}")
    
    entrada_cidade = input(">>> ").strip()
    codigo_cidade = obter_codigo_cidade(estado, entrada_cidade)
    
    # Obter tipo de imóvel
    print("\n🏠 DIGITE O TIPO DE IMÓVEL (1=Casa, 2=Apartamento, 4=Indiferente):")
    tipo_imovel = input(">>> ").strip()
    if tipo_imovel == "":
        tipo_imovel = "4"
    
    # Obter faixa de valor
    print("\n💰 DIGITE A FAIXA DE VALOR (1-7, ou Enter para Indiferente):")
    faixa_valor = input(">>> ").strip()
    if faixa_valor == "":
        faixa_valor = None
    
    # Obter quartos
    print("\n🛏️ DIGITE O NÚMERO DE QUARTOS (1-4, ou Enter para Indiferente):")
    quartos = input(">>> ").strip()
    if quartos == "":
        quartos = None
    
    # Mostrar resumo
    print("\n" + "="*60)
    print("📋 RESUMO DOS FILTROS")
    print("="*60)
    print(f"Estado: {estado}")
    print(f"Código da Cidade: {codigo_cidade}")
    print(f"Tipo de Imóvel: {tipo_imovel}")
    print(f"Faixa de Valor: {faixa_valor if faixa_valor else 'Indiferente'}")
    print(f"Quartos: {quartos if quartos else 'Indiferente'}")
    
    # Confirmar
    print("\nDeseja executar a busca? (s/n):")
    confirmacao = input(">>> ").lower().strip()
    
    if confirmacao not in ['s', 'sim', 'y', 'yes']:
        print("Busca cancelada!")
        return
    
    # Executar busca
    print("\n🚀 Executando busca...")
    
    chrome_options = Options()
    chrome_options.add_argument("--window-size=1920,1080")
    
    service = Service(ChromeDriverManager().install())
    driver = webdriver.Chrome(service=service, options=chrome_options)
    
    try:
        # Acessar página inicial
        driver.get(URL)
        print("Acessando página de busca...")
        time.sleep(3)
        
        # Selecionar estado
        print(f"Selecionando estado: {estado}")
        select_estado = Select(driver.find_element(By.ID, "cmb_estado"))
        select_estado.select_by_value(estado)
        time.sleep(2)
        
        # Selecionar cidade
        print(f"Selecionando cidade: {codigo_cidade}")
        select_cidade = Select(driver.find_element(By.ID, "cmb_cidade"))
        select_cidade.select_by_value(codigo_cidade)
        time.sleep(2)
        
        # Clicar no primeiro botão "Próximo"
        print("Clicando no botão 'Próximo'...")
        try:
            btn_next = driver.find_element(By.ID, "btn_next0")
            btn_next.click()
        except Exception as e:
            driver.execute_script("document.getElementById('btn_next0').click();")
        
        time.sleep(3)
        
        # Aplicar filtros adicionais
        if tipo_imovel:
            try:
                select_tipo = Select(driver.find_element(By.ID, "cmb_tp_imovel"))
                select_tipo.select_by_value(tipo_imovel)
                print(f"Tipo de imóvel selecionado: {tipo_imovel}")
                time.sleep(1)
            except Exception as e:
                print(f"Erro ao selecionar tipo: {e}")
        
        if quartos:
            try:
                select_quartos = Select(driver.find_element(By.ID, "cmb_quartos"))
                select_quartos.select_by_value(quartos)
                print(f"Quartos selecionados: {quartos}")
                time.sleep(1)
            except Exception as e:
                print(f"Erro ao selecionar quartos: {e}")
        
        if faixa_valor:
            try:
                select_valor = Select(driver.find_element(By.ID, "cmb_faixa_vlr"))
                select_valor.select_by_value(faixa_valor)
                print(f"Faixa de valor selecionada: {faixa_valor}")
                time.sleep(1)
            except Exception as e:
                print(f"Erro ao selecionar valor: {e}")
        
        # Clicar no segundo botão "Próximo"
        print("Clicando no segundo botão 'Próximo'...")
        try:
            btn_next2 = driver.find_element(By.ID, "btn_next1")
            btn_next2.click()
        except Exception as e:
            driver.execute_script("document.getElementById('btn_next1').click();")
        
        print("Aguardando carregamento dos resultados...")
        time.sleep(10)
        
        # Extrair dados
        print("Procurando por imóveis...")
        
        seletores_imoveis = [".group-block-item"]
        imoveis = []
        
        for seletor in seletores_imoveis:
            try:
                elementos = driver.find_elements(By.CSS_SELECTOR, seletor)
                print(f"Encontrados {len(elementos)} elementos")
                
                for i, elemento in enumerate(elementos, 1):
                    try:
                        link_element = elemento.find_element(By.CSS_SELECTOR, "a[onclick*='detalhe_imovel']")
                        texto_completo = link_element.text.strip()
                        
                        # Extrair dados com regex
                        match = re.search(r'([^-]+) - (.+?) \| R\$ (.+)', texto_completo)
                        
                        if match:
                            cidade = match.group(1).strip()
                            nome_imovel = match.group(2).strip()
                            valor = match.group(3).strip()
                            
                            # Extrair ID
                            onclick = link_element.get_attribute('onclick')
                            id_match = re.search(r'detalhe_imovel\((\d+)\)', onclick)
                            id_imovel = id_match.group(1) if id_match else ''
                            
                            imovel = {
                                'numero': i,
                                'cidade': cidade,
                                'nome_imovel': nome_imovel,
                                'valor': valor,
                                'id_imovel': id_imovel
                            }
                            imoveis.append(imovel)
                            print(f"  Imóvel {i}: {nome_imovel} - R$ {valor}")
                    
                    except Exception as e:
                        print(f"Erro ao processar imóvel {i}: {e}")
                
                if imoveis:
                    break
                    
            except Exception as e:
                print(f"Erro com seletor: {e}")
        
        # Salvar resultados
        if imoveis:
            df = pd.DataFrame(imoveis)
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            
            filename = f"imoveis_{estado.lower()}_{timestamp}.csv"
            df.to_csv(filename, index=False, encoding='utf-8-sig')
            print(f"\n✅ Dados salvos em: {filename}")
            
            print(f"\n🎉 Total de imóveis encontrados: {len(imoveis)}")
            
            # Mostrar resumo
            print("\n📊 RESUMO DOS IMÓVEIS:")
            print("-" * 50)
            for imovel in imoveis:
                print(f"  {imovel['numero']}. {imovel['nome_imovel']}")
                print(f"     Cidade: {imovel['cidade']}")
                print(f"     Valor: R$ {imovel['valor']}")
                print(f"     ID: {imovel['id_imovel']}")
                print()
        else:
            print("\n❌ Nenhum imóvel encontrado")
        
        # Salvar screenshot
        screenshot_filename = f"screenshot_{estado.lower()}_{timestamp}.png"
        driver.save_screenshot(screenshot_filename)
        print(f"📸 Screenshot salvo: {screenshot_filename}")
        
    except Exception as e:
        print(f"❌ Erro durante a execução: {e}")
        
    finally:
        print("Fechando navegador...")
        driver.quit()

if __name__ == "__main__":
    main() 