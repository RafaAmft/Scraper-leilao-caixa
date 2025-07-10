import requests
from bs4 import BeautifulSoup
import pandas as pd
from datetime import datetime
import time
import json
import re

class CaixaImoveisScraperFinal:
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
    
    def buscar_imoveis_joinville(self):
        """Busca imóveis em Joinville usando requests"""
        try:
            print("Iniciando busca de imóveis em Joinville, SC...")
            
            # Primeiro, vamos acessar a página inicial
            response = self.session.get(
                self.base_url,
                headers=self.headers,
                timeout=30
            )
            
            if response.status_code == 200:
                print("Página inicial acessada com sucesso!")
                
                # Agora tenta fazer a busca
                params = {
                    'sltTipoBusca': 'imoveis',
                    'sltEstado': 'SC',
                    'sltCidade': 'JOINVILLE',
                    'btnBuscar': 'Buscar'
                }
                
                print("Fazendo busca com parâmetros...")
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
                    return response.text
            else:
                print(f"Erro ao acessar o site: {response.status_code}")
                return None
                
        except Exception as e:
            print(f"Erro ao fazer a busca: {e}")
            return None
    
    def analisar_conteudo(self, html):
        """Analisa o conteúdo da página para entender a estrutura"""
        soup = BeautifulSoup(html, 'html.parser')
        
        print("=== ANÁLISE DO CONTEÚDO ===")
        
        # Procura por texto que contenha informações de imóveis
        texto_completo = soup.get_text()
        
        # Palavras-chave que indicam dados de imóveis
        keywords_imoveis = [
            'código', 'tipo', 'endereço', 'bairro', 'valor', 'leilão', 'imóvel',
            'casa', 'apartamento', 'terreno', 'comercial', 'residencial',
            'R$', 'reais', 'valor mínimo', 'valor máximo'
        ]
        
        print("Procurando por palavras-chave relacionadas a imóveis...")
        for keyword in keywords_imoveis:
            if keyword.lower() in texto_completo.lower():
                print(f"✓ Encontrada: {keyword}")
        
        # Procura por padrões de endereços
        padroes_endereco = [
            r'Rua\s+[A-Za-z\s]+,\s*\d+',
            r'Av\.\s+[A-Za-z\s]+,\s*\d+',
            r'Bairro\s+[A-Za-z\s]+',
            r'Joinville,\s*SC'
        ]
        
        print("\nProcurando por padrões de endereços...")
        for padrao in padroes_endereco:
            matches = re.findall(padrao, texto_completo, re.IGNORECASE)
            if matches:
                print(f"✓ Padrão encontrado: {padrao}")
                for match in matches[:3]:  # Mostra apenas os primeiros 3
                    print(f"  - {match}")
        
        # Procura por valores monetários
        padrao_valor = r'R\$\s*[\d.,]+'
        valores = re.findall(padrao_valor, texto_completo)
        if valores:
            print(f"\n✓ Encontrados {len(valores)} valores monetários:")
            for valor in valores[:5]:  # Mostra apenas os primeiros 5
                print(f"  - {valor}")
        
        return soup
    
    def extrair_dados_imoveis(self, html):
        """Extrai os dados dos imóveis do HTML"""
        try:
            soup = BeautifulSoup(html, 'html.parser')
            
            print("\n=== EXTRAINDO DADOS DE IMÓVEIS ===")
            
            # Analisa o conteúdo primeiro
            self.analisar_conteudo(html)
            
            # Procura por elementos que possam conter dados de imóveis
            elementos_imoveis = []
            
            # Procura por divs com classes específicas
            divs_imoveis = soup.find_all('div', class_=re.compile(r'(imovel|resultado|item|card)', re.I))
            elementos_imoveis.extend(divs_imoveis)
            
            # Procura por spans com dados
            spans_dados = soup.find_all('span', string=re.compile(r'(R\$|Joinville|SC|Código|Tipo)', re.I))
            elementos_imoveis.extend(spans_dados)
            
            # Procura por parágrafos com informações
            paragrafos = soup.find_all('p', string=re.compile(r'(Rua|Av\.|Bairro|Joinville)', re.I))
            elementos_imoveis.extend(paragrafos)
            
            # Procura por listas
            listas = soup.find_all(['ul', 'ol'])
            for lista in listas:
                itens = lista.find_all('li')
                for item in itens:
                    texto = item.get_text(strip=True)
                    if any(keyword in texto.lower() for keyword in ['rua', 'av.', 'bairro', 'joinville', 'r$']):
                        elementos_imoveis.append(item)
            
            print(f"Encontrados {len(elementos_imoveis)} elementos potenciais de imóveis")
            
            # Processa os elementos encontrados
            for i, elemento in enumerate(elementos_imoveis):
                texto = elemento.get_text(strip=True)
                
                # Filtra apenas elementos com informações relevantes
                if len(texto) > 20 and any(keyword in texto.lower() for keyword in ['rua', 'av.', 'bairro', 'joinville', 'r$', 'código']):
                    # Extrai informações usando regex
                    codigo_match = re.search(r'Código[:\s]*(\d+)', texto, re.I)
                    tipo_match = re.search(r'Tipo[:\s]*([A-Za-z\s]+)', texto, re.I)
                    endereco_match = re.search(r'(Rua|Av\.)\s+([A-Za-z\s,]+)', texto, re.I)
                    valor_match = re.search(r'R\$\s*([\d.,]+)', texto)
                    
                    imovel = {
                        'codigo': codigo_match.group(1) if codigo_match else '',
                        'tipo': tipo_match.group(1).strip() if tipo_match else '',
                        'endereco': endereco_match.group(0) if endereco_match else texto[:100],
                        'bairro': '',
                        'valor': valor_match.group(1) if valor_match else '',
                        'data_leilao': '',
                        'cidade': 'Joinville',
                        'estado': 'SC',
                        'data_extracao': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
                        'texto_completo': texto[:200]  # Guarda o texto completo para análise
                    }
                    
                    self.imoveis.append(imovel)
                    print(f"Imóvel {i+1} extraído: {imovel['codigo']} - {imovel['endereco'][:50]}...")
            
            # Se não encontrou nada específico, tenta extrair qualquer informação útil
            if not self.imoveis:
                print("Nenhum imóvel específico encontrado. Extraindo informações gerais...")
                
                # Procura por qualquer texto que pareça ser de imóvel
                texto_completo = soup.get_text()
                linhas = texto_completo.split('\n')
                
                for linha in linhas:
                    linha = linha.strip()
                    if len(linha) > 30 and any(keyword in linha.lower() for keyword in ['joinville', 'rua', 'av.', 'bairro', 'r$']):
                        imovel = {
                            'codigo': '',
                            'tipo': '',
                            'endereco': linha[:100],
                            'bairro': '',
                            'valor': '',
                            'data_leilao': '',
                            'cidade': 'Joinville',
                            'estado': 'SC',
                            'data_extracao': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
                            'texto_completo': linha
                        }
                        self.imoveis.append(imovel)
            
            print(f"\nTotal de imóveis extraídos: {len(self.imoveis)}")
            
        except Exception as e:
            print(f"Erro ao extrair dados: {e}")
    
    def salvar_resultados(self, formato='csv'):
        """Salva os resultados em arquivo"""
        if not self.imoveis:
            print("Nenhum imóvel encontrado para salvar")
            return
        
        df = pd.DataFrame(self.imoveis)
        
        if formato == 'csv':
            filename = f"imoveis_joinville_final_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv"
            df.to_csv(filename, index=False, encoding='utf-8-sig')
            print(f"Resultados salvos em: {filename}")
        
        elif formato == 'json':
            filename = f"imoveis_joinville_final_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
            df.to_json(filename, orient='records', indent=2, force_ascii=False)
            print(f"Resultados salvos em: {filename}")
    
    def executar_busca(self):
        """Executa a busca completa"""
        try:
            print("=== SCRAPER FINAL - IMÓVEIS CAIXA JOINVILLE ===")
            
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
                    
                    # Mostra um resumo dos dados
                    print("\n=== RESUMO DOS DADOS ===")
                    for i, imovel in enumerate(self.imoveis[:3], 1):  # Mostra apenas os primeiros 3
                        print(f"\nImóvel {i}:")
                        print(f"  Código: {imovel['codigo']}")
                        print(f"  Tipo: {imovel['tipo']}")
                        print(f"  Endereço: {imovel['endereco']}")
                        print(f"  Valor: {imovel['valor']}")
                else:
                    print("Nenhum imóvel encontrado")
            else:
                print("Falha na busca")
                
        except Exception as e:
            print(f"Erro durante a execução: {e}")

def main():
    scraper = CaixaImoveisScraperFinal()
    scraper.executar_busca()

if __name__ == "__main__":
    main() 