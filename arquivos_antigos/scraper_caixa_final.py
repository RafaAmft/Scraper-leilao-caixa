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

def extrair_dados_imovel(elemento):
    """Extrai dados de um elemento de imóvel"""
    try:
        # Procurar pelo link com os dados do imóvel
        link_element = elemento.find_element(By.CSS_SELECTOR, "a[onclick*='detalhe_imovel']")
        texto_completo = link_element.text.strip()
        
        # Extrair informações usando regex
        # Padrão: "JOINVILLE - NOME DO IMÓVEL | R$ VALOR"
        match = re.search(r'JOINVILLE - (.+?) \| R\$ (.+)', texto_completo)
        
        if match:
            nome_imovel = match.group(1).strip()
            valor = match.group(2).strip()
            
            # Extrair ID do imóvel do onclick
            onclick = link_element.get_attribute('onclick')
            id_match = re.search(r'detalhe_imovel\((\d+)\)', onclick)
            id_imovel = id_match.group(1) if id_match else ''
            
            # Extrair URL da imagem
            try:
                img_element = elemento.find_element(By.CSS_SELECTOR, "img.fotoimovel")
                url_imagem = img_element.get_attribute('src')
            except:
                url_imagem = ''
            
            return {
                'id_imovel': id_imovel,
                'nome_imovel': nome_imovel,
                'valor': valor,
                'url_imagem': url_imagem,
                'texto_completo': texto_completo
            }
        else:
            return None
            
    except Exception as e:
        print(f"Erro ao extrair dados do imóvel: {e}")
        return None

def main():
    chrome_options = Options()
    chrome_options.add_argument("--window-size=1920,1080")
    
    service = Service(ChromeDriverManager().install())
    driver = webdriver.Chrome(service=service, options=chrome_options)
    
    try:
        print("🚀 Iniciando busca final de imóveis em Joinville/SC...")
        
        # Acessar página inicial
        driver.get(URL)
        print("Acessando página de busca...")
        time.sleep(3)
        
        # Selecionar estado
        print("Selecionando estado: SC")
        select_estado = Select(driver.find_element(By.ID, "cmb_estado"))
        select_estado.select_by_value("SC")
        time.sleep(2)
        
        # Selecionar cidade
        print("Selecionando cidade: JOINVILLE")
        select_cidade = Select(driver.find_element(By.ID, "cmb_cidade"))
        select_cidade.select_by_value("8690")
        time.sleep(2)
        
        # Clicar no primeiro botão "Próximo"
        print("Clicando no botão 'Próximo'...")
        try:
            btn_next = driver.find_element(By.ID, "btn_next0")
            btn_next.click()
        except Exception as e:
            driver.execute_script("document.getElementById('btn_next0').click();")
        
        time.sleep(3)
        
        # Clicar no segundo botão "Próximo" sem filtros
        print("Clicando no segundo botão 'Próximo'...")
        try:
            btn_next2 = driver.find_element(By.ID, "btn_next1")
            btn_next2.click()
        except Exception as e:
            driver.execute_script("document.getElementById('btn_next1').click();")
        
        print("Aguardando carregamento dos resultados...")
        time.sleep(10)
        
        # Procurar por elementos de imóveis
        print("Procurando por imóveis na página...")
        
        # Tentar diferentes seletores para encontrar os elementos de imóveis
        seletores_imoveis = [
            ".group-block-item",
            "li[class*='group-block-item']",
            ".dadosimovel-col2",
            "ul[class*='form-set'] li"
        ]
        
        imoveis = []
        
        for seletor in seletores_imoveis:
            try:
                elementos = driver.find_elements(By.CSS_SELECTOR, seletor)
                print(f"Seletor '{seletor}': {len(elementos)} elementos encontrados")
                
                if len(elementos) > 0:
                    for i, elemento in enumerate(elementos, 1):
                        dados = extrair_dados_imovel(elemento)
                        if dados:
                            dados['numero'] = i
                            imoveis.append(dados)
                            print(f"  Imóvel {i}: {dados['nome_imovel']} - R$ {dados['valor']}")
                    
                    if imoveis:
                        break  # Se encontrou imóveis, para de tentar outros seletores
                        
            except Exception as e:
                print(f"Erro com seletor '{seletor}': {e}")
        
        # Se não encontrou com os seletores específicos, tentar extrair do HTML
        if not imoveis:
            print("Tentando extrair dados diretamente do HTML...")
            
            # Procurar por padrões no HTML
            page_source = driver.page_source
            
            # Padrão para encontrar imóveis no HTML
            padrao_imoveis = r'JOINVILLE - ([^|]+) \| R\$ ([^<]+)'
            matches = re.findall(padrao_imoveis, page_source)
            
            for i, match in enumerate(matches, 1):
                nome_imovel = match[0].strip()
                valor = match[1].strip()
                
                imovel = {
                    'numero': i,
                    'nome_imovel': nome_imovel,
                    'valor': valor,
                    'id_imovel': '',
                    'url_imagem': '',
                    'texto_completo': f"JOINVILLE - {nome_imovel} | R$ {valor}"
                }
                imoveis.append(imovel)
                print(f"  Imóvel {i}: {nome_imovel} - R$ {valor}")
        
        # Salvar resultados
        if imoveis:
            df = pd.DataFrame(imoveis)
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            
            filename = f"imoveis_joinville_final_{timestamp}.csv"
            df.to_csv(filename, index=False, encoding='utf-8-sig')
            print(f"\n✅ Dados salvos em: {filename}")
            
            json_filename = f"imoveis_joinville_final_{timestamp}.json"
            df.to_json(json_filename, orient='records', force_ascii=False, indent=2)
            print(f"✅ Dados salvos em JSON: {json_filename}")
            
            print(f"\n🎉 Total de imóveis encontrados: {len(imoveis)}")
            
            # Mostrar resumo
            print("\n📊 RESUMO DOS IMÓVEIS:")
            print("-" * 50)
            for imovel in imoveis:
                print(f"  {imovel['numero']}. {imovel['nome_imovel']}")
                print(f"     Valor: R$ {imovel['valor']}")
                print(f"     ID: {imovel['id_imovel']}")
                print()
        else:
            print("\n❌ Nenhum imóvel encontrado")
            
            # Salvar HTML para análise
            html_filename = f"pagina_sem_resultados_{datetime.now().strftime('%Y%m%d_%H%M%S')}.html"
            with open(html_filename, 'w', encoding='utf-8') as f:
                f.write(driver.page_source)
            print(f"📄 HTML salvo para análise: {html_filename}")
        
        # Salvar screenshot
        screenshot_filename = f"screenshot_final_{datetime.now().strftime('%Y%m%d_%H%M%S')}.png"
        driver.save_screenshot(screenshot_filename)
        print(f"📸 Screenshot salvo: {screenshot_filename}")
        
    except Exception as e:
        print(f"❌ Erro durante a execução: {e}")
        
    finally:
        print("Fechando navegador...")
        driver.quit()

if __name__ == "__main__":
    main() 