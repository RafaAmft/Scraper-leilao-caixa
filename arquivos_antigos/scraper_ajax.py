import requests
from bs4 import BeautifulSoup
import pandas as pd
from datetime import datetime
import time
import json
import re

class CaixaImoveisScraperAjax:
    def __init__(self):
        self.base_url = "https://venda-imoveis.caixa.gov.br/sistema"
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
            'X-Requested-With': 'XMLHttpRequest',  # Para requisições AJAX
        }
    
    def buscar_imoveis_joinville(self):
        """Busca imóveis em Joinville usando requisições AJAX"""
        try:
            print("Iniciando busca de imóveis em Joinville, SC...")
            
            # Primeiro, vamos acessar a página inicial para obter cookies
            response = self.session.get(
                f"{self.base_url}/busca-imovel.asp",
                headers=self.headers,
                timeout=30
            )
            
            if response.status_code == 200:
                print("Página inicial acessada com sucesso!")
                
                # Agora vamos tentar acessar diretamente a página de resultados
                # Baseado na análise do HTML, vamos tentar diferentes URLs
                
                # Método 1: Tentar acessar a página de resultados diretamente
                urls_teste = [
                    f"{self.base_url}/venda-online/resultados.asp",
                    f"{self.base_url}/venda-online/detalhe-imovel.asp",
                    f"{self.base_url}/venda-online/favoritos.asp",
                ]
                
                for url in urls_teste:
                    print(f"Testando URL: {url}")
                    try:
                        response_resultados = self.session.get(
                            url,
                            headers=self.headers,
                            timeout=30
                        )
                        
                        if response_resultados.status_code == 200:
                            print(f"✓ URL acessada com sucesso: {url}")
                            return response_resultados.text
                        else:
                            print(f"✗ Erro ao acessar {url}: {response_resultados.status_code}")
                            
                    except Exception as e:
                        print(f"✗ Erro ao acessar {url}: {e}")
                
                # Método 2: Tentar fazer POST para carregar resultados
                print("\nTentando carregar resultados via POST...")
                
                # Parâmetros baseados na análise do JavaScript
                params_post = {
                    'hdn_estado': 'SC',
                    'hdn_cidade': 'JOINVILLE',
                    'hdn_modalidade': '',
                    'hdn_bairro': '',
                    'hdn_nobairro': '',
                    'hdn_tp_imovel': 'Indiferente',
                    'hdn_quartos': 'Indiferente',
                    'hdn_vg_garagem': 'Indiferente',
                    'hdn_area_util': 'Indiferente',
                    'hdn_faixa_vlr': 'Indiferente',
                    'hdnQtdPag': '1',
                    'hdnPagNum': '1'
                }
                
                response_post = self.session.post(
                    f"{self.base_url}/venda-online/resultados.asp",
                    data=params_post,
                    headers=self.headers,
                    timeout=30
                )
                
                if response_post.status_code == 200:
                    print("✓ Resultados carregados via POST")
                    return response_post.text
                else:
                    print(f"✗ Erro no POST: {response_post.status_code}")
                
                # Se nada funcionou, retorna a página inicial para análise
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
            'R$', 'reais', 'valor mínimo', 'valor máximo', 'joinville'
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
        
        # Procura por tabelas de resultados
        tabelas = soup.find_all('table')
        print(f"\nTabelas encontradas: {len(tabelas)}")
        
        for i, tabela in enumerate(tabelas):
            print(f"\n--- Tabela {i+1} ---")
            linhas = tabela.find_all('tr')
            print(f"Linhas: {len(linhas)}")
            
            if linhas:
                # Mostra cabeçalho
                cabecalho = linhas[0]
                cols = cabecalho.find_all(['th', 'td'])
                print("Cabeçalho:", [col.get_text(strip=True) for col in cols])
                
                # Mostra primeira linha de dados
                if len(linhas) > 1:
                    primeira_linha = linhas[1]
                    cols = primeira_linha.find_all(['th', 'td'])
                    print("Primeira linha:", [col.get_text(strip=True) for col in cols])
        
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
            filename = f"imoveis_joinville_ajax_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv"
            df.to_csv(filename, index=False, encoding='utf-8-sig')
            print(f"Resultados salvos em: {filename}")
        
        elif formato == 'json':
            filename = f"imoveis_joinville_ajax_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
            df.to_json(filename, orient='records', indent=2, force_ascii=False)
            print(f"Resultados salvos em: {filename}")
    
    def executar_busca(self):
        """Executa a busca completa"""
        try:
            print("=== SCRAPER AJAX - IMÓVEIS CAIXA JOINVILLE ===")
            
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
    scraper = CaixaImoveisScraperAjax()
    scraper.executar_busca()

if __name__ == "__main__":
    main() 