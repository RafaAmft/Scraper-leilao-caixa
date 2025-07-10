import time
import pandas as pd
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
from bs4 import BeautifulSoup
import json
import re
from datetime import datetime

class CaixaImoveisScraper:
    def __init__(self):
        self.base_url = "https://venda-imoveis.caixa.gov.br/sistema/busca-imovel.asp?sltTipoBusca=imoveis"
        self.driver = None
        self.imoveis = []
        
    def setup_driver(self):
        """Configura o driver do Chrome com opções otimizadas"""
        chrome_options = Options()
        chrome_options.add_argument("--no-sandbox")
        chrome_options.add_argument("--disable-dev-shm-usage")
        chrome_options.add_argument("--disable-gpu")
        chrome_options.add_argument("--window-size=1920,1080")
        # chrome_options.add_argument("--headless")  # Descomente para executar sem interface gráfica
        
        service = Service(ChromeDriverManager().install())
        self.driver = webdriver.Chrome(service=service, options=chrome_options)
        
    def buscar_imoveis_joinville(self):
        """Busca imóveis em Joinville, SC"""
        try:
            print("Iniciando busca de imóveis em Joinville, SC...")
            
            # Acessa a página inicial
            self.driver.get(self.base_url)
            time.sleep(3)
            
            # Aguarda a página carregar
            wait = WebDriverWait(self.driver, 10)
            
            # Seleciona o estado (Santa Catarina)
            try:
                estado_select = wait.until(EC.element_to_be_clickable((By.NAME, "sltEstado")))
                self.driver.execute_script("arguments[0].value = 'SC';", estado_select)
                time.sleep(1)
                
                # Seleciona a cidade (Joinville)
                cidade_select = wait.until(EC.element_to_be_clickable((By.NAME, "sltCidade")))
                self.driver.execute_script("arguments[0].value = 'JOINVILLE';", cidade_select)
                time.sleep(1)
                
                # Clica no botão de buscar
                buscar_btn = wait.until(EC.element_to_be_clickable((By.NAME, "btnBuscar")))
                buscar_btn.click()
                time.sleep(5)
                
                print("Busca realizada com sucesso!")
                return True
                
            except Exception as e:
                print(f"Erro ao selecionar estado/cidade: {e}")
                return False
                
        except Exception as e:
            print(f"Erro ao acessar o site: {e}")
            return False
    
    def extrair_dados_imoveis(self):
        """Extrai os dados dos imóveis da página atual"""
        try:
            # Aguarda a tabela de resultados carregar
            wait = WebDriverWait(self.driver, 10)
            tabela = wait.until(EC.presence_of_element_located((By.CLASS_NAME, "tabela")))
            
            # Obtém o HTML da página
            html = self.driver.page_source
            soup = BeautifulSoup(html, 'html.parser')
            
            # Encontra a tabela de resultados
            tabela_element = soup.find('table', class_='tabela')
            if not tabela_element:
                print("Tabela de resultados não encontrada")
                return
            
            # Extrai as linhas da tabela (excluindo o cabeçalho)
            linhas = tabela_element.find_all('tr')[1:]  # Pula o cabeçalho
            
            for linha in linhas:
                colunas = linha.find_all('td')
                if len(colunas) >= 6:
                    imovel = {
                        'codigo': colunas[0].get_text(strip=True),
                        'tipo': colunas[1].get_text(strip=True),
                        'endereco': colunas[2].get_text(strip=True),
                        'bairro': colunas[3].get_text(strip=True),
                        'valor': colunas[4].get_text(strip=True),
                        'data_leilao': colunas[5].get_text(strip=True),
                        'cidade': 'Joinville',
                        'estado': 'SC',
                        'data_extracao': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                    }
                    self.imoveis.append(imovel)
            
            print(f"Extraídos {len(linhas)} imóveis da página atual")
            
        except Exception as e:
            print(f"Erro ao extrair dados: {e}")
    
    def navegar_paginas(self):
        """Navega por todas as páginas de resultados"""
        pagina = 1
        while True:
            print(f"Processando página {pagina}...")
            
            # Extrai dados da página atual
            self.extrair_dados_imoveis()
            
            # Tenta ir para a próxima página
            try:
                wait = WebDriverWait(self.driver, 5)
                proxima_btn = wait.until(EC.element_to_be_clickable((By.LINK_TEXT, "Próxima")))
                proxima_btn.click()
                time.sleep(3)
                pagina += 1
            except:
                print("Não há mais páginas para processar")
                break
    
    def salvar_resultados(self, formato='csv'):
        """Salva os resultados em arquivo"""
        if not self.imoveis:
            print("Nenhum imóvel encontrado para salvar")
            return
        
        df = pd.DataFrame(self.imoveis)
        
        if formato == 'csv':
            filename = f"imoveis_joinville_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv"
            df.to_csv(filename, index=False, encoding='utf-8-sig')
            print(f"Resultados salvos em: {filename}")
        
        elif formato == 'json':
            filename = f"imoveis_joinville_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
            df.to_json(filename, orient='records', indent=2, force_ascii=False)
            print(f"Resultados salvos em: {filename}")
        
        elif formato == 'excel':
            filename = f"imoveis_joinville_{datetime.now().strftime('%Y%m%d_%H%M%S')}.xlsx"
            df.to_excel(filename, index=False)
            print(f"Resultados salvos em: {filename}")
    
    def executar_busca_completa(self):
        """Executa a busca completa de imóveis"""
        try:
            print("=== SCRAPER DE IMÓVEIS CAIXA - JOINVILLE ===")
            
            # Configura o driver
            self.setup_driver()
            
            # Realiza a busca
            if self.buscar_imoveis_joinville():
                # Navega por todas as páginas
                self.navegar_paginas()
                
                # Salva os resultados
                if self.imoveis:
                    print(f"\nTotal de imóveis encontrados: {len(self.imoveis)}")
                    self.salvar_resultados('csv')
                    self.salvar_resultados('json')
                    self.salvar_resultados('excel')
                else:
                    print("Nenhum imóvel encontrado")
            else:
                print("Falha na busca inicial")
                
        except Exception as e:
            print(f"Erro durante a execução: {e}")
        
        finally:
            if self.driver:
                self.driver.quit()
                print("Driver fechado")

def main():
    scraper = CaixaImoveisScraper()
    scraper.executar_busca_completa()

if __name__ == "__main__":
    main() 