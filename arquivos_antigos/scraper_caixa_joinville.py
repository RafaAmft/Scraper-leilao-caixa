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

# Parâmetros de busca
ESTADO = "SC"
CIDADE_VALOR = "8690"  # Valor correto para Joinville
CIDADE_TEXTO = "JOINVILLE"
TIPO_IMOVEL = "2"  # 2 = Apartamento, 1 = Casa, 4 = Indiferente

def main():
    chrome_options = Options()
    chrome_options.add_argument("--window-size=1920,1080")
    # chrome_options.add_argument("--headless")  # Descomente para executar sem interface gráfica
    
    service = Service(ChromeDriverManager().install())
    driver = webdriver.Chrome(service=service, options=chrome_options)
    
    try:
        print("🚀 Iniciando busca de imóveis em Joinville/SC...")
        
        # Acessar página inicial
        driver.get(URL)
        print("Acessando página de busca...")
        time.sleep(3)
        
        # Selecionar estado
        print(f"Selecionando estado: {ESTADO}")
        select_estado = Select(driver.find_element(By.ID, "cmb_estado"))
        select_estado.select_by_value(ESTADO)
        time.sleep(2)
        
        # Selecionar cidade usando o valor correto
        print(f"Selecionando cidade: {CIDADE_TEXTO} (valor: {CIDADE_VALOR})")
        select_cidade = Select(driver.find_element(By.ID, "cmb_cidade"))
        select_cidade.select_by_value(CIDADE_VALOR)
        time.sleep(2)
        
        # Clicar no botão "Próximo" com tratamento para elemento interceptado
        print("Clicando no botão 'Próximo'...")
        try:
            # Tentar clicar diretamente
            btn_next = driver.find_element(By.ID, "btn_next0")
            btn_next.click()
        except Exception as e:
            print(f"Botão interceptado, tentando JavaScript...")
            # Usar JavaScript para clicar
            driver.execute_script("document.getElementById('btn_next0').click();")
        
        time.sleep(3)
        
        # Agora os outros campos devem estar visíveis
        print("Preenchendo filtros adicionais...")
        
        # Selecionar tipo de imóvel (se disponível)
        try:
            select_tipo = Select(driver.find_element(By.ID, "cmb_tp_imovel"))
            select_tipo.select_by_value(TIPO_IMOVEL)
            print(f"Tipo de imóvel selecionado: {TIPO_IMOVEL}")
            time.sleep(1)
        except Exception as e:
            print(f"Campo tipo de imóvel não encontrado: {e}")
        
        # Selecionar quartos (se disponível)
        try:
            select_quartos = Select(driver.find_element(By.ID, "cmb_quartos"))
            select_quartos.select_by_value("4")  # 4+ quartos
            print("Quartos selecionados: 4+")
            time.sleep(1)
        except Exception as e:
            print(f"Campo quartos não encontrado: {e}")
        
        # Selecionar área útil (se disponível)
        try:
            select_area = Select(driver.find_element(By.ID, "cmb_area_util"))
            select_area.select_by_value("3")  # 100-150m²
            print("Área útil selecionada: 100-150m²")
            time.sleep(1)
        except Exception as e:
            print(f"Campo área útil não encontrado: {e}")
        
        # Selecionar faixa de valor (se disponível)
        try:
            select_valor = Select(driver.find_element(By.ID, "cmb_faixa_vlr"))
            select_valor.select_by_value("5")  # 200-300k
            print("Faixa de valor selecionada: 200-300k")
            time.sleep(1)
        except Exception as e:
            print(f"Campo faixa de valor não encontrado: {e}")
        
        # Clicar no segundo botão "Próximo" com tratamento
        print("Clicando no segundo botão 'Próximo'...")
        try:
            btn_next2 = driver.find_element(By.ID, "btn_next1")
            btn_next2.click()
        except Exception as e:
            print(f"Segundo botão interceptado, tentando JavaScript...")
            driver.execute_script("document.getElementById('btn_next1').click();")
        
        time.sleep(5)
        
        # Aguardar carregamento dos resultados
        print("Aguardando carregamento dos resultados...")
        wait = WebDriverWait(driver, 20)
        
        # Verificar se há resultados
        try:
            resultados = driver.find_elements(By.CSS_SELECTOR, "table tr")
            print(f"Encontrados {len(resultados)} elementos na tabela")
            
            if len(resultados) > 1:  # Mais de 1 porque a primeira linha é o cabeçalho
                print("✅ Resultados encontrados!")
                
                # Extrair dados dos imóveis
                imoveis = []
                for i, linha in enumerate(resultados[1:], 1):  # Pular cabeçalho
                    try:
                        colunas = linha.find_elements(By.TAG_NAME, "td")
                        if len(colunas) >= 4:
                            imovel = {
                                'numero': i,
                                'endereco': colunas[0].text.strip() if colunas[0].text else '',
                                'tipo': colunas[1].text.strip() if len(colunas) > 1 and colunas[1].text else '',
                                'valor': colunas[2].text.strip() if len(colunas) > 2 and colunas[2].text else '',
                                'detalhes': colunas[3].text.strip() if len(colunas) > 3 and colunas[3].text else ''
                            }
                            imoveis.append(imovel)
                            print(f"Imóvel {i}: {imovel['endereco']} - {imovel['valor']}")
                    except Exception as e:
                        print(f"Erro ao processar linha {i}: {e}")
                
                # Salvar resultados
                if imoveis:
                    df = pd.DataFrame(imoveis)
                    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
                    filename = f"imoveis_joinville_caixa_{timestamp}.csv"
                    df.to_csv(filename, index=False, encoding='utf-8-sig')
                    print(f"✅ Dados salvos em: {filename}")
                    
                    # Salvar também em JSON
                    json_filename = f"imoveis_joinville_caixa_{timestamp}.json"
                    df.to_json(json_filename, orient='records', force_ascii=False, indent=2)
                    print(f"✅ Dados salvos em JSON: {json_filename}")
                else:
                    print("❌ Nenhum imóvel encontrado")
            else:
                print("❌ Nenhum resultado encontrado")
                
        except Exception as e:
            print(f"Erro ao processar resultados: {e}")
        
        # Salvar screenshot
        screenshot_filename = f"screenshot_resultados_{datetime.now().strftime('%Y%m%d_%H%M%S')}.png"
        driver.save_screenshot(screenshot_filename)
        print(f"📸 Screenshot salvo: {screenshot_filename}")
        
        # Salvar HTML da página
        html_filename = f"pagina_resultados_{datetime.now().strftime('%Y%m%d_%H%M%S')}.html"
        with open(html_filename, 'w', encoding='utf-8') as f:
            f.write(driver.page_source)
        print(f"📄 HTML salvo: {html_filename}")
        
    except Exception as e:
        print(f"❌ Erro durante a execução: {e}")
        
    finally:
        print("Fechando navegador...")
        driver.quit()

if __name__ == "__main__":
    main() 