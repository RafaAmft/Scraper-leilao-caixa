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

def buscar_imoveis_com_filtros(driver, filtros):
    """Busca imóveis com filtros específicos"""
    
    print(f"\n🔍 Tentando com filtros: {filtros}")
    
    try:
        # Selecionar estado
        select_estado = Select(driver.find_element(By.ID, "cmb_estado"))
        select_estado.select_by_value(ESTADO)
        time.sleep(2)
        
        # Selecionar cidade
        select_cidade = Select(driver.find_element(By.ID, "cmb_cidade"))
        select_cidade.select_by_value(CIDADE_VALOR)
        time.sleep(2)
        
        # Clicar no primeiro botão "Próximo"
        try:
            btn_next = driver.find_element(By.ID, "btn_next0")
            btn_next.click()
        except Exception as e:
            driver.execute_script("document.getElementById('btn_next0').click();")
        
        time.sleep(3)
        
        # Aplicar filtros se especificados
        if 'tipo_imovel' in filtros:
            try:
                select_tipo = Select(driver.find_element(By.ID, "cmb_tp_imovel"))
                select_tipo.select_by_value(filtros['tipo_imovel'])
                print(f"  Tipo de imóvel: {filtros['tipo_imovel']}")
                time.sleep(1)
            except Exception as e:
                print(f"  Erro ao selecionar tipo: {e}")
        
        if 'quartos' in filtros:
            try:
                select_quartos = Select(driver.find_element(By.ID, "cmb_quartos"))
                select_quartos.select_by_value(filtros['quartos'])
                print(f"  Quartos: {filtros['quartos']}")
                time.sleep(1)
            except Exception as e:
                print(f"  Erro ao selecionar quartos: {e}")
        
        if 'area_util' in filtros:
            try:
                select_area = Select(driver.find_element(By.ID, "cmb_area_util"))
                select_area.select_by_value(filtros['area_util'])
                print(f"  Área útil: {filtros['area_util']}")
                time.sleep(1)
            except Exception as e:
                print(f"  Erro ao selecionar área: {e}")
        
        if 'faixa_valor' in filtros:
            try:
                select_valor = Select(driver.find_element(By.ID, "cmb_faixa_vlr"))
                select_valor.select_by_value(filtros['faixa_valor'])
                print(f"  Faixa de valor: {filtros['faixa_valor']}")
                time.sleep(1)
            except Exception as e:
                print(f"  Erro ao selecionar valor: {e}")
        
        # Clicar no segundo botão "Próximo"
        try:
            btn_next2 = driver.find_element(By.ID, "btn_next1")
            btn_next2.click()
        except Exception as e:
            driver.execute_script("document.getElementById('btn_next1').click();")
        
        time.sleep(5)
        
        # Verificar se há resultados
        resultados = driver.find_elements(By.CSS_SELECTOR, "table tr")
        
        # Verificar se há mensagem de "nenhum imóvel encontrado"
        page_source = driver.page_source
        if "Nenhum imóvel encontrado" in page_source:
            print("  ❌ Nenhum imóvel encontrado")
            return False, []
        
        if len(resultados) > 1:
            print(f"  ✅ Encontrados {len(resultados)-1} imóveis!")
            
            # Extrair dados dos imóveis
            imoveis = []
            for i, linha in enumerate(resultados[1:], 1):
                try:
                    colunas = linha.find_elements(By.TAG_NAME, "td")
                    if len(colunas) >= 4:
                        imovel = {
                            'numero': i,
                            'endereco': colunas[0].text.strip() if colunas[0].text else '',
                            'tipo': colunas[1].text.strip() if len(colunas) > 1 and colunas[1].text else '',
                            'valor': colunas[2].text.strip() if len(colunas) > 2 and colunas[2].text else '',
                            'detalhes': colunas[3].text.strip() if len(colunas) > 3 and colunas[3].text else '',
                            'filtros_usados': str(filtros)
                        }
                        imoveis.append(imovel)
                        print(f"    Imóvel {i}: {imovel['endereco']} - {imovel['valor']}")
                except Exception as e:
                    print(f"    Erro ao processar linha {i}: {e}")
            
            return True, imoveis
        else:
            print("  ❌ Nenhum resultado na tabela")
            return False, []
            
    except Exception as e:
        print(f"  ❌ Erro durante a busca: {e}")
        return False, []

def main():
    chrome_options = Options()
    chrome_options.add_argument("--window-size=1920,1080")
    
    service = Service(ChromeDriverManager().install())
    driver = webdriver.Chrome(service=service, options=chrome_options)
    
    try:
        print("🚀 Iniciando busca de imóveis em Joinville/SC...")
        
        # Acessar página inicial
        driver.get(URL)
        print("Acessando página de busca...")
        time.sleep(3)
        
        # Lista de combinações de filtros para tentar
        combinacoes_filtros = [
            {},  # Sem filtros - apenas estado e cidade
            {'tipo_imovel': '4'},  # Indiferente
            {'tipo_imovel': '2'},  # Apartamento
            {'tipo_imovel': '1'},  # Casa
            {'faixa_valor': '1'},  # Até 50k
            {'faixa_valor': '2'},  # 50-100k
            {'faixa_valor': '3'},  # 100-150k
            {'faixa_valor': '4'},  # 150-200k
            {'faixa_valor': '5'},  # 200-300k
            {'area_util': '1'},    # Até 50m²
            {'area_util': '2'},    # 50-100m²
            {'area_util': '3'},    # 100-150m²
            {'quartos': '1'},      # 1 quarto
            {'quartos': '2'},      # 2 quartos
            {'quartos': '3'},      # 3 quartos
            {'quartos': '4'},      # 4+ quartos
        ]
        
        todos_imoveis = []
        
        for i, filtros in enumerate(combinacoes_filtros, 1):
            print(f"\n{'='*60}")
            print(f"TENTATIVA {i}/{len(combinacoes_filtros)}")
            print(f"{'='*60}")
            
            # Recarregar página para cada tentativa
            driver.get(URL)
            time.sleep(3)
            
            sucesso, imoveis = buscar_imoveis_com_filtros(driver, filtros)
            
            if sucesso and imoveis:
                todos_imoveis.extend(imoveis)
                print(f"✅ Encontrados {len(imoveis)} imóveis com estes filtros!")
                
                # Salvar resultados parciais
                timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
                df_parcial = pd.DataFrame(imoveis)
                filename_parcial = f"imoveis_joinville_parcial_{i}_{timestamp}.csv"
                df_parcial.to_csv(filename_parcial, index=False, encoding='utf-8-sig')
                print(f"📄 Dados parciais salvos: {filename_parcial}")
        
        # Salvar todos os resultados
        if todos_imoveis:
            df_final = pd.DataFrame(todos_imoveis)
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            
            filename_final = f"imoveis_joinville_final_{timestamp}.csv"
            df_final.to_csv(filename_final, index=False, encoding='utf-8-sig')
            print(f"\n✅ Dados finais salvos: {filename_final}")
            
            json_filename = f"imoveis_joinville_final_{timestamp}.json"
            df_final.to_json(json_filename, orient='records', force_ascii=False, indent=2)
            print(f"✅ Dados finais salvos em JSON: {json_filename}")
            
            print(f"\n🎉 Total de imóveis encontrados: {len(todos_imoveis)}")
        else:
            print("\n❌ Nenhum imóvel encontrado com nenhuma combinação de filtros")
        
        # Salvar screenshot final
        screenshot_filename = f"screenshot_final_{datetime.now().strftime('%Y%m%d_%H%M%S')}.png"
        driver.save_screenshot(screenshot_filename)
        print(f"📸 Screenshot final salvo: {screenshot_filename}")
        
    except Exception as e:
        print(f"❌ Erro durante a execução: {e}")
        
    finally:
        print("Fechando navegador...")
        driver.quit()

if __name__ == "__main__":
    main() 