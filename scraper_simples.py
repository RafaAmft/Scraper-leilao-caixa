import requests
from bs4 import BeautifulSoup
import pandas as pd
from datetime import datetime
import time
import json

class CaixaImoveisScraperSimples:
    def __init__(self):
        self.base_url = "https://venda-imoveis.caixa.gov.br/sistema/busca-imovel.asp"
        self.session = requests.Session()
        self.imoveis = []
        
        # Headers para simular um navegador real
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
            'Accept-Language': 'pt-BR,pt;q=0.9,en;q=0.8',
            'Accept-Encoding': 'gzip, deflate, br',
            'Connection': 'keep-alive',
            'Upgrade-Insecure-Requests': '1',
        }
    
    def buscar_imoveis_joinville(self):
        """Busca imóveis em Joinville usando requests"""
        try:
            print("Iniciando busca de imóveis em Joinville, SC...")
            
            # Parâmetros da busca
            params = {
                'sltTipoBusca': 'imoveis',
                'sltEstado': 'SC',
                'sltCidade': 'JOINVILLE',
                'btnBuscar': 'Buscar'
            }
            
            # Faz a requisição
            response = self.session.get(
                self.base_url,
                params=params,
                headers=self.headers,
                timeout=30
            )
            
            if response.status_code == 200:
                print("Busca realizada com sucesso!")
                return response.text
            else:
                print(f"Erro na requisição: {response.status_code}")
                return None
                
        except Exception as e:
            print(f"Erro ao fazer a busca: {e}")
            return None
    
    def extrair_dados_imoveis(self, html):
        """Extrai os dados dos imóveis do HTML"""
        try:
            soup = BeautifulSoup(html, 'html.parser')
            
            # Procura por diferentes possíveis estruturas de tabela
            tabela = soup.find('table', class_='tabela')
            if not tabela:
                tabela = soup.find('table', {'border': '1'})
            if not tabela:
                tabela = soup.find('table')
            
            if not tabela:
                print("Tabela de resultados não encontrada")
                return
            
            # Extrai as linhas da tabela
            linhas = tabela.find_all('tr')
            
            for linha in linhas[1:]:  # Pula o cabeçalho
                colunas = linha.find_all(['td', 'th'])
                
                if len(colunas) >= 4:
                    # Tenta extrair os dados baseado na estrutura esperada
                    dados = [col.get_text(strip=True) for col in colunas]
                    
                    # Cria um dicionário com os dados extraídos
                    imovel = {
                        'codigo': dados[0] if len(dados) > 0 else '',
                        'tipo': dados[1] if len(dados) > 1 else '',
                        'endereco': dados[2] if len(dados) > 2 else '',
                        'bairro': dados[3] if len(dados) > 3 else '',
                        'valor': dados[4] if len(dados) > 4 else '',
                        'data_leilao': dados[5] if len(dados) > 5 else '',
                        'cidade': 'Joinville',
                        'estado': 'SC',
                        'data_extracao': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                    }
                    
                    self.imoveis.append(imovel)
            
            print(f"Extraídos {len(linhas)-1} imóveis")
            
        except Exception as e:
            print(f"Erro ao extrair dados: {e}")
    
    def salvar_resultados(self, formato='csv'):
        """Salva os resultados em arquivo"""
        if not self.imoveis:
            print("Nenhum imóvel encontrado para salvar")
            return
        
        df = pd.DataFrame(self.imoveis)
        
        if formato == 'csv':
            filename = f"imoveis_joinville_simples_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv"
            df.to_csv(filename, index=False, encoding='utf-8-sig')
            print(f"Resultados salvos em: {filename}")
        
        elif formato == 'json':
            filename = f"imoveis_joinville_simples_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
            df.to_json(filename, orient='records', indent=2, force_ascii=False)
            print(f"Resultados salvos em: {filename}")
    
    def executar_busca(self):
        """Executa a busca completa"""
        try:
            print("=== SCRAPER SIMPLES - IMÓVEIS CAIXA JOINVILLE ===")
            
            # Faz a busca
            html = self.buscar_imoveis_joinville()
            
            if html:
                # Extrai os dados
                self.extrair_dados_imoveis(html)
                
                # Salva os resultados
                if self.imoveis:
                    print(f"\nTotal de imóveis encontrados: {len(self.imoveis)}")
                    self.salvar_resultados('csv')
                    self.salvar_resultados('json')
                else:
                    print("Nenhum imóvel encontrado")
            else:
                print("Falha na busca")
                
        except Exception as e:
            print(f"Erro durante a execução: {e}")

def main():
    scraper = CaixaImoveisScraperSimples()
    scraper.executar_busca()

if __name__ == "__main__":
    main() 