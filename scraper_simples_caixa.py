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

URL = "https://venda-imoveis.caixa.gov.br/sistema/busca-imovel.asp?sltTipoBusca=imoveis"

def main():
    chrome_options = Options()
    chrome_options.add_argument("--window-size=1920,1080")
    
    service = Service(ChromeDriverManager().install())
    driver = webdriver.Chrome(service=service, options=chrome_options)
    
    try:
        print("🚀 Iniciando busca simples de imóveis em Joinville/SC...")
        
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
        time.sleep(10)  # Aguardar mais tempo para carregar
        
        # Tentar diferentes seletores para encontrar os imóveis
        print("Procurando por imóveis na página...")
        
        imoveis = []
        
        # Tentar diferentes seletores
        seletores = [
            "table tr",
            ".imovel-item",
            ".card-imovel", 
            ".resultado-imovel",
            "tr[class*='imovel']",
            ".lista-imoveis tr",
            "tbody tr"
        ]
        
        for seletor in seletores:
            try:
                elementos = driver.find_elements(By.CSS_SELECTOR, seletor)
                print(f"Seletor '{seletor}': {len(elementos)} elementos encontrados")
                
                if len(elementos) > 1:  # Mais de 1 porque pode ter cabeçalho
                    for i, elemento in enumerate(elementos[1:], 1):  # Pular primeiro elemento (cabeçalho)
                        try:
                            # Tentar extrair dados de diferentes formas
                            colunas = elemento.find_elements(By.TAG_NAME, "td")
                            
                            if len(colunas) >= 2:
                                imovel = {
                                    'numero': i,
                                    'endereco': colunas[0].text.strip() if colunas[0].text else '',
                                    'tipo': colunas[1].text.strip() if len(colunas) > 1 and colunas[1].text else '',
                                    'valor': colunas[2].text.strip() if len(colunas) > 2 and colunas[2].text else '',
                                    'detalhes': colunas[3].text.strip() if len(colunas) > 3 and colunas[3].text else '',
                                    'seletor_usado': seletor
                                }
                                imoveis.append(imovel)
                                print(f"  Imóvel {i}: {imovel['endereco']} - {imovel['valor']}")
                            
                        except Exception as e:
                            print(f"  Erro ao processar elemento {i}: {e}")
                    
                    if imoveis:
                        break  # Se encontrou imóveis, para de tentar outros seletores
                        
            except Exception as e:
                print(f"Erro com seletor '{seletor}': {e}")
        
        # Salvar resultados
        if imoveis:
            df = pd.DataFrame(imoveis)
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            
            filename = f"imoveis_joinville_simples_{timestamp}.csv"
            df.to_csv(filename, index=False, encoding='utf-8-sig')
            print(f"\n✅ Dados salvos em: {filename}")
            
            json_filename = f"imoveis_joinville_simples_{timestamp}.json"
            df.to_json(json_filename, orient='records', force_ascii=False, indent=2)
            print(f"✅ Dados salvos em JSON: {json_filename}")
            
            print(f"\n🎉 Total de imóveis encontrados: {len(imoveis)}")
        else:
            print("\n❌ Nenhum imóvel encontrado")
            
            # Salvar HTML para análise
            html_filename = f"pagina_sem_resultados_{datetime.now().strftime('%Y%m%d_%H%M%S')}.html"
            with open(html_filename, 'w', encoding='utf-8') as f:
                f.write(driver.page_source)
            print(f"📄 HTML salvo para análise: {html_filename}")
        
        # Salvar screenshot
        screenshot_filename = f"screenshot_simples_{datetime.now().strftime('%Y%m%d_%H%M%S')}.png"
        driver.save_screenshot(screenshot_filename)
        print(f"📸 Screenshot salvo: {screenshot_filename}")
        
    except Exception as e:
        print(f"❌ Erro durante a execução: {e}")
        
    finally:
        print("Fechando navegador...")
        driver.quit()

if __name__ == "__main__":
    main() 