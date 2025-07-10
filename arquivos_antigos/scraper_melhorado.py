import requests
from bs4 import BeautifulSoup
import pandas as pd
from datetime import datetime
import time
import json
import re

class CaixaImoveisScraperMelhorado:
    def __init__(self):
        self.base_url = "https://venda-imoveis.caixa.gov.br/sistema/busca-imovel.asp"
        self.session = requests.Session()
        self.imoveis = []
        
        # Headers mais completos
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
            'Accept-Language': 'pt-BR,pt;q=0.9,en;q=0.8',
            'Accept-Encoding': 'gzip, deflate, br',
            'Connection': 'keep-alive',
            'Upgrade-Insecure-Requests': '1',
            'Sec-Fetch-Dest': 'document',
            'Sec-Fetch-Mode': 'navigate',
            'Sec-Fetch-Site': 'none',
            'Cache-Control': 'max-age=0',
        }
    
    def analisar_estrutura_site(self, html):
        """Analisa a estrutura do site para entender como extrair os dados"""
        soup = BeautifulSoup(html, 'html.parser')
        
        print("=== ANÁLISE DA ESTRUTURA DO SITE ===")
        
        # Procura por todas as tabelas
        tabelas = soup.find_all('table')
        print(f"Encontradas {len(tabelas)} tabelas no site")
        
        for i, tabela in enumerate(tabelas):
            print(f"\n--- Tabela {i+1} ---")
            print(f"Classes: {tabela.get('class', 'Nenhuma')}")
            print(f"ID: {tabela.get('id', 'Nenhum')}")
            print(f"Border: {tabela.get('border', 'Nenhum')}")
            
            # Mostra as primeiras linhas
            linhas = tabela.find_all('tr')
            print(f"Número de linhas: {len(linhas)}")
            
            if linhas:
                # Mostra cabeçalho
                cabecalho = linhas[0]
                cols_cabecalho = cabecalho.find_all(['th', 'td'])
                print("Cabeçalho:", [col.get_text(strip=True) for col in cols_cabecalho])
                
                # Mostra primeira linha de dados
                if len(linhas) > 1:
                    primeira_linha = linhas[1]
                    cols_dados = primeira_linha.find_all(['th', 'td'])
                    print("Primeira linha:", [col.get_text(strip=True) for col in cols_dados])
        
        # Procura por divs que possam conter dados
        divs_importantes = soup.find_all('div', class_=re.compile(r'(resultado|imovel|dados)', re.I))
        print(f"\nDivs importantes encontradas: {len(divs_importantes)}")
        
        for div in divs_importantes:
            print(f"Div: {div.get('class')} - Texto: {div.get_text(strip=True)[:100]}...")
        
        # Procura por links que possam ser de imóveis
        links_imoveis = soup.find_all('a', href=re.compile(r'imovel|detalhe', re.I))
        print(f"\nLinks de imóveis encontrados: {len(links_imoveis)}")
        
        return soup
    
    def buscar_imoveis_joinville(self):
        """Busca imóveis em Joinville usando requests"""
        try:
            print("Iniciando busca de imóveis em Joinville, SC...")
            
            # Primeiro, vamos acessar a página inicial para entender a estrutura
            response = self.session.get(
                self.base_url,
                headers=self.headers,
                timeout=30
            )
            
            if response.status_code == 200:
                print("Página inicial acessada com sucesso!")
                
                # Analisa a estrutura
                soup = self.analisar_estrutura_site(response.text)
                
                # Agora tenta fazer a busca
                params = {
                    'sltTipoBusca': 'imoveis',
                    'sltEstado': 'SC',
                    'sltCidade': 'JOINVILLE',
                    'btnBuscar': 'Buscar'
                }
                
                print("\nFazendo busca com parâmetros...")
                response_busca = self.session.post(
                    self.base_url,
                    data=params,
                    headers=self.headers,
                    timeout=30
                )
                
                if response_busca.status_code == 200:
                    print("Busca realizada com sucesso!")
                    return response_busca.text
                else:
                    print(f"Erro na busca: {response_busca.status_code}")
                    return response.text  # Retorna a página inicial para análise
            else:
                print(f"Erro ao acessar o site: {response.status_code}")
                return None
                
        except Exception as e:
            print(f"Erro ao fazer a busca: {e}")
            return None
    
    def extrair_dados_imoveis(self, html):
        """Extrai os dados dos imóveis do HTML"""
        try:
            soup = BeautifulSoup(html, 'html.parser')
            
            print("\n=== TENTANDO EXTRAIR DADOS ===")
            
            # Tenta diferentes estratégias para encontrar os dados
            
            # Estratégia 1: Procurar por tabelas com dados de imóveis
            tabelas = soup.find_all('table')
            for tabela in tabelas:
                linhas = tabela.find_all('tr')
                if len(linhas) > 1:  # Tem pelo menos cabeçalho e uma linha de dados
                    print(f"Analisando tabela com {len(linhas)} linhas")
                    
                    # Verifica se parece ser uma tabela de imóveis
                    primeira_linha = linhas[0]
                    cols = primeira_linha.find_all(['th', 'td'])
                    texto_cols = [col.get_text(strip=True).lower() for col in cols]
                    
                    # Palavras-chave que indicam que é uma tabela de imóveis
                    keywords = ['código', 'tipo', 'endereço', 'bairro', 'valor', 'leilão', 'imóvel']
                    matches = sum(1 for keyword in keywords if any(keyword in col for col in texto_cols))
                    
                    if matches >= 2:  # Pelo menos 2 colunas fazem sentido
                        print("Tabela de imóveis encontrada!")
                        self.extrair_dados_tabela(linhas)
                        return
            
            # Estratégia 2: Procurar por divs com dados de imóveis
            divs_imoveis = soup.find_all('div', class_=re.compile(r'imovel|resultado', re.I))
            if divs_imoveis:
                print(f"Encontrados {len(divs_imoveis)} divs de imóveis")
                self.extrair_dados_divs(divs_imoveis)
                return
            
            # Estratégia 3: Procurar por listas
            listas = soup.find_all(['ul', 'ol'])
            for lista in listas:
                itens = lista.find_all('li')
                if len(itens) > 0:
                    print(f"Lista encontrada com {len(itens)} itens")
                    self.extrair_dados_lista(itens)
                    return
            
            print("Nenhuma estrutura de dados de imóveis encontrada")
            
        except Exception as e:
            print(f"Erro ao extrair dados: {e}")
    
    def extrair_dados_tabela(self, linhas):
        """Extrai dados de uma tabela"""
        for i, linha in enumerate(linhas[1:], 1):  # Pula o cabeçalho
            colunas = linha.find_all(['td', 'th'])
            
            if len(colunas) >= 4:
                dados = [col.get_text(strip=True) for col in colunas]
                
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
                print(f"Imóvel {i} extraído: {imovel['codigo']} - {imovel['tipo']}")
        
        print(f"Total de imóveis extraídos da tabela: {len(self.imoveis)}")
    
    def extrair_dados_divs(self, divs):
        """Extrai dados de divs"""
        for div in divs:
            texto = div.get_text(strip=True)
            if len(texto) > 10:  # Texto significativo
                imovel = {
                    'codigo': '',
                    'tipo': '',
                    'endereco': texto[:100],
                    'bairro': '',
                    'valor': '',
                    'data_leilao': '',
                    'cidade': 'Joinville',
                    'estado': 'SC',
                    'data_extracao': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                }
                self.imoveis.append(imovel)
        
        print(f"Total de imóveis extraídos dos divs: {len(self.imoveis)}")
    
    def extrair_dados_lista(self, itens):
        """Extrai dados de uma lista"""
        for item in itens:
            texto = item.get_text(strip=True)
            if len(texto) > 10:
                imovel = {
                    'codigo': '',
                    'tipo': '',
                    'endereco': texto[:100],
                    'bairro': '',
                    'valor': '',
                    'data_leilao': '',
                    'cidade': 'Joinville',
                    'estado': 'SC',
                    'data_extracao': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                }
                self.imoveis.append(imovel)
        
        print(f"Total de imóveis extraídos da lista: {len(self.imoveis)}")
    
    def salvar_resultados(self, formato='csv'):
        """Salva os resultados em arquivo"""
        if not self.imoveis:
            print("Nenhum imóvel encontrado para salvar")
            return
        
        df = pd.DataFrame(self.imoveis)
        
        if formato == 'csv':
            filename = f"imoveis_joinville_melhorado_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv"
            df.to_csv(filename, index=False, encoding='utf-8-sig')
            print(f"Resultados salvos em: {filename}")
        
        elif formato == 'json':
            filename = f"imoveis_joinville_melhorado_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
            df.to_json(filename, orient='records', indent=2, force_ascii=False)
            print(f"Resultados salvos em: {filename}")
    
    def executar_busca(self):
        """Executa a busca completa"""
        try:
            print("=== SCRAPER MELHORADO - IMÓVEIS CAIXA JOINVILLE ===")
            
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
    scraper = CaixaImoveisScraperMelhorado()
    scraper.executar_busca()

if __name__ == "__main__":
    main() 