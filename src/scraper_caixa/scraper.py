import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support.select import Select
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
import pandas as pd
from datetime import datetime
import re
import os

def configurar_chromedriver(headless=True):
    """Configura o ChromeDriver de forma robusta para funcionar em diferentes ambientes"""
    chrome_options = Options()
    chrome_options.add_argument("--window-size=1920,1080")
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")
    chrome_options.add_argument("--disable-gpu")
    
    if headless:
        chrome_options.add_argument("--headless")
    
    # Configuração mais robusta do ChromeDriver
    try:
        # Tentar usar ChromeDriverManager primeiro
        driver_path = ChromeDriverManager().install()
        print(f"🔧 ChromeDriver encontrado em: {driver_path}")
        
        # Verificar se o arquivo é executável
        if not os.path.isfile(driver_path):
            raise Exception(f"ChromeDriver não encontrado em: {driver_path}")
            
        service = Service(driver_path)
        driver = webdriver.Chrome(service=service, options=chrome_options)
        return driver
        
    except Exception as e:
        print(f"⚠️ Erro com ChromeDriverManager: {e}")
        print("🔄 Tentando configuração alternativa...")
        
        try:
            # Tentar usar ChromeDriver do sistema
            driver = webdriver.Chrome(options=chrome_options)
            return driver
        except Exception as e2:
            print(f"❌ Erro com Chrome do sistema: {e2}")
            print("🔄 Tentando configuração manual...")
            
            # Última tentativa: usar caminho padrão do sistema
            try:
                service = Service("/usr/bin/chromedriver")
                driver = webdriver.Chrome(service=service, options=chrome_options)
                return driver
            except Exception as e3:
                print(f"❌ Falha total ao configurar ChromeDriver: {e3}")
                raise Exception(f"Não foi possível configurar o ChromeDriver: {e3}")

URL = "https://venda-imoveis.caixa.gov.br/sistema/busca-imovel.asp?sltTipoBusca=imoveis"

# Dicionário atualizado com códigos verificados do site
ESTADOS_CIDADES = {
    "SC": {"8690": "JOINVILLE", "8621": "FLORIANOPOLIS", "8545": "BLUMENAU", "8558": "BRUSQUE", "8598": "CRICIUMA", "8564": "CAMBORIU", "8687": "JARAGUA DO SUL", "8500": "BARRA VELHA", "8510": "BALNEARIO PICARRAS", "8520": "ITAJAI", "8530": "GOVERNADOR CELSO RAMOS"},
    "SP": {"3550308": "SAO PAULO", "3509502": "CAMPINAS", "3548708": "SANTOS", "3543402": "RIBEIRAO PRETO", "3506607": "BARUERI", "3548500": "SANTO ANDRE"},
    "RS": {"4314902": "PORTO ALEGRE", "4304606": "CAXIAS DO SUL", "4316907": "SANTA MARIA", "4320000": "PELOTAS", "4307005": "GRAVATAI"},
    "PR": {"4106902": "CURITIBA", "4113700": "LONDRINA", "4104808": "CASCAVEL", "4115200": "MARINGA", "4101804": "APUCARANA"},
    "MG": {"3106200": "BELO HORIZONTE", "3170206": "UBERLANDIA", "3149309": "POUSO ALEGRE", "3136702": "JUIZ DE FORA"},
    "RJ": {"3304557": "RIO DE JANEIRO", "3303500": "NOVA IGUACU", "3301702": "DUQUE DE CAXIAS", "3303302": "NITEROI"},
    "BA": {"2927408": "SALVADOR", "2910800": "FEIRA DE SANTANA", "2921005": "ILHEUS", "2929206": "VITORIA DA CONQUISTA"},
    "CE": {"2304400": "FORTALEZA", "2303709": "CAUCAIA", "2307650": "JUAZEIRO DO NORTE", "2312908": "SOBRAL"},
    "PE": {"2611606": "RECIFE", "2609600": "JABOATAO DOS GUARARAPES", "2607901": "PETROPOLIS"},
    "GO": {"5208707": "GOIANIA", "5201405": "ANAPOLIS", "5218806": "RIO VERDE", "5201108": "AGUAS LINDAS DE GOIAS"},
    "MT": {"5103403": "CUIABA", "5102504": "CACERES", "5107602": "RONDONOPOLIS"},
    "MS": {"5002704": "CAMPO GRANDE", "5003207": "CORUMBA", "5004106": "DOURADOS"}
}

# Opções de filtros
TIPOS_IMOVEL = {
    "1": "Casa",
    "2": "Apartamento", 
    "4": "Indiferente"
}

FAIXAS_VALOR = {
    "1": "Até R$ 50.000",
    "2": "R$ 50.000 a R$ 100.000",
    "3": "R$ 100.000 a R$ 150.000", 
    "4": "R$ 150.000 a R$ 200.000",
    "5": "R$ 200.000 a R$ 300.000",
    "6": "R$ 300.000 a R$ 500.000",
    "7": "Acima de R$ 500.000"
}

QUARTOS = {
    "1": "1 quarto",
    "2": "2 quartos",
    "3": "3 quartos", 
    "4": "4+ quartos"
}

def mostrar_menu():
    """Mostra o menu de opções para o usuário"""
    print("\n" + "="*60)
    print("🏠 SCRAPER INTERATIVO - IMÓVEIS CAIXA")
    print("="*60)
    
    # Mostrar estados disponíveis
    print("\n📍 ESTADOS DISPONÍVEIS:")
    for i, estado in enumerate(ESTADOS_CIDADES.keys(), 1):
        print(f"  {i}. {estado}")
    
    # Mostrar tipos de imóvel
    print("\n🏠 TIPOS DE IMÓVEL:")
    for codigo, tipo in TIPOS_IMOVEL.items():
        print(f"  {codigo}. {tipo}")
    
    # Mostrar faixas de valor
    print("\n💰 FAIXAS DE VALOR:")
    for codigo, faixa in FAIXAS_VALOR.items():
        print(f"  {codigo}. {faixa}")
    
    # Mostrar quartos
    print("\n🛏️ QUARTOS:")
    for codigo, quarto in QUARTOS.items():
        print(f"  {codigo}. {quarto}")

def obter_entrada_usuario():
    """Obtém as entradas do usuário"""
    print("\n" + "="*60)
    print("🔧 CONFIGURAÇÃO DOS FILTROS")
    print("="*60)
    
    # Selecionar estado
    print("\n📍 SELECIONE O ESTADO:")
    for i, estado in enumerate(ESTADOS_CIDADES.keys(), 1):
        print(f"  {i}. {estado}")
    
    while True:
        try:
            escolha_estado = int(input("\nDigite o número do estado: "))
            if 1 <= escolha_estado <= len(ESTADOS_CIDADES):
                estado = list(ESTADOS_CIDADES.keys())[escolha_estado - 1]
                break
            else:
                print("❌ Opção inválida! Tente novamente.")
        except ValueError:
            print("❌ Digite um número válido!")
    
    # Selecionar cidade
    print(f"\n🏙️ CIDADES DISPONÍVEIS EM {estado}:")
    cidades = ESTADOS_CIDADES[estado]
    for i, (codigo, nome) in enumerate(cidades.items(), 1):
        print(f"  {i}. {nome}")
    
    while True:
        try:
            escolha_cidade = int(input("\nDigite o número da cidade: "))
            if 1 <= escolha_cidade <= len(cidades):
                codigo_cidade = list(cidades.keys())[escolha_cidade - 1]
                nome_cidade = list(cidades.values())[escolha_cidade - 1]
                break
            else:
                print("❌ Opção inválida! Tente novamente.")
        except ValueError:
            print("❌ Digite um número válido!")
    
    # Selecionar tipo de imóvel
    print("\n🏠 SELECIONE O TIPO DE IMÓVEL:")
    for codigo, tipo in TIPOS_IMOVEL.items():
        print(f"  {codigo}. {tipo}")
    
    while True:
        tipo_imovel = input("\nDigite o código do tipo de imóvel (ou Enter para 'Indiferente'): ").strip()
        if tipo_imovel == "":
            tipo_imovel = "4"  # Indiferente
            break
        elif tipo_imovel in TIPOS_IMOVEL:
            break
        else:
            print("❌ Código inválido! Tente novamente.")
    
    # Selecionar faixa de valor
    print("\n💰 SELECIONE A FAIXA DE VALOR:")
    for codigo, faixa in FAIXAS_VALOR.items():
        print(f"  {codigo}. {faixa}")
    
    while True:
        faixa_valor = input("\nDigite o código da faixa de valor (ou Enter para 'Indiferente'): ").strip()
        if faixa_valor == "":
            faixa_valor = None
            break
        elif faixa_valor in FAIXAS_VALOR:
            break
        else:
            print("❌ Código inválido! Tente novamente.")
    
    # Selecionar quartos
    print("\n🛏️ SELECIONE O NÚMERO DE QUARTOS:")
    for codigo, quarto in QUARTOS.items():
        print(f"  {codigo}. {quarto}")
    
    while True:
        quartos = input("\nDigite o código de quartos (ou Enter para 'Indiferente'): ").strip()
        if quartos == "":
            quartos = None
            break
        elif quartos in QUARTOS:
            break
        else:
            print("❌ Código inválido! Tente novamente.")
    
    return {
        'estado': estado,
        'codigo_cidade': codigo_cidade,
        'nome_cidade': nome_cidade,
        'tipo_imovel': tipo_imovel,
        'faixa_valor': faixa_valor,
        'quartos': quartos
    }

def extrair_dados_imovel(elemento):
    """Extrai dados de um elemento de imóvel"""
    try:
        # Procurar pelo link com os dados do imóvel
        link_element = elemento.find_element(By.CSS_SELECTOR, "a[onclick*='detalhe_imovel']")
        texto_completo = link_element.text.strip()
        
        # Extrair informações usando regex
        # Padrão: "CIDADE - NOME DO IMÓVEL | R$ VALOR"
        match = re.search(r'([^-]+) - (.+?) \| R\$ (.+)', texto_completo)
        
        if match:
            cidade = match.group(1).strip()
            nome_imovel = match.group(2).strip()
            valor = match.group(3).strip()
            
            # Extrair ID do imóvel do onclick
            onclick = link_element.get_attribute('onclick')
            id_match = re.search(r'detalhe_imovel\((\d+)\)', onclick)
            id_imovel = id_match.group(1) if id_match else ''
            
            # Gerar link direto para o imóvel
            link_direto = f"https://venda-imoveis.caixa.gov.br/sistema/detalhe-imovel.asp?hdnOrigem=index&txtImovel={id_imovel}" if id_imovel else ''
            
            # Extrair URL da imagem
            try:
                img_element = elemento.find_element(By.CSS_SELECTOR, "img.fotoimovel")
                url_imagem = img_element.get_attribute('src')
            except:
                url_imagem = ''
            
            # Tentar extrair informações adicionais do elemento pai
            endereco = ''
            quartos = ''
            
            try:
                # Procurar por informações de endereço e quartos no texto do elemento
                texto_elemento = elemento.text
                
                # Padrões para extrair endereço (pode variar dependendo do site)
                endereco_patterns = [
                    r'Endereço[:\s]+([^\n]+)',
                    r'Localização[:\s]+([^\n]+)',
                    r'Bairro[:\s]+([^\n]+)',
                    r'Rua[:\s]+([^\n]+)',
                    r'Av[:\s]+([^\n]+)'
                ]
                
                for pattern in endereco_patterns:
                    endereco_match = re.search(pattern, texto_elemento, re.IGNORECASE)
                    if endereco_match:
                        endereco = endereco_match.group(1).strip()
                        break
                
                # Padrões para extrair quartos
                quartos_patterns = [
                    r'(\d+)\s*quarto',
                    r'(\d+)\s*suíte',
                    r'(\d+)\s*dormitório',
                    r'(\d+)\s*bedroom'
                ]
                
                for pattern in quartos_patterns:
                    quartos_match = re.search(pattern, texto_elemento, re.IGNORECASE)
                    if quartos_match:
                        quartos = quartos_match.group(1)
                        break
                        
            except Exception as e:
                print(f"Erro ao extrair informações adicionais: {e}")
            
            return {
                'id_imovel': id_imovel,
                'cidade': cidade,
                'nome_imovel': nome_imovel,
                'valor': valor,
                'endereco': endereco,
                'quartos': quartos,
                'url_imagem': url_imagem,
                'link_direto': link_direto,
                'texto_completo': texto_completo
            }
        else:
            return None
            
    except Exception as e:
        print(f"Erro ao extrair dados do imóvel: {e}")
        return None

def extrair_imoveis_da_pagina(driver, filtros, numero_pagina=1):
    """Extrai imóveis de uma página específica"""
    print(f"\n📄 Extraindo imóveis da página {numero_pagina}...")
    
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
                        dados['pagina'] = numero_pagina
                        dados['filtros_usados'] = str(filtros)
                        imoveis.append(dados)
                        print(f"  Imóvel {i} (página {numero_pagina}): {dados['nome_imovel']} - R$ {dados['valor']}")
                
                if imoveis:
                    break
                    
        except Exception as e:
            print(f"Erro com seletor '{seletor}': {e}")
    
    # Se não encontrou com os seletores específicos, tentar extrair do HTML
    if not imoveis:
        print("Tentando extrair dados diretamente do HTML...")
        
        page_source = driver.page_source
        padrao_imoveis = r'([^-]+) - ([^|]+) \| R\$ ([^<]+)'
        matches = re.findall(padrao_imoveis, page_source)
        
        for i, match in enumerate(matches, 1):
            cidade = match[0].strip()
            nome_imovel = match[1].strip()
            valor = match[2].strip()
            
            imovel = {
                'numero': i,
                'pagina': numero_pagina,
                'cidade': cidade,
                'nome_imovel': nome_imovel,
                'valor': valor,
                'id_imovel': '',
                'url_imagem': '',
                'texto_completo': f"{cidade} - {nome_imovel} | R$ {valor}",
                'filtros_usados': str(filtros)
            }
            imoveis.append(imovel)
            print(f"  Imóvel {i} (página {numero_pagina}): {nome_imovel} - R$ {valor}")
    
    return imoveis

def verificar_proxima_pagina(driver):
    """Verifica se existe uma próxima página e retorna o botão"""
    try:
        # Verificar se há mensagem de "nenhum resultado"
        mensagens_sem_resultado = driver.find_elements(By.XPATH, 
            "//*[contains(text(), 'Nenhum resultado') or contains(text(), 'nenhum resultado') or contains(text(), 'Não foram encontrados')]")
        
        if mensagens_sem_resultado:
            print("🔍 Detectada mensagem de 'nenhum resultado'")
            return None
        
        # Verificar se há elementos de imóveis na página
        elementos_imoveis = driver.find_elements(By.CSS_SELECTOR, "a[onclick*='detalhe_imovel']")
        if not elementos_imoveis:
            print("🔍 Nenhum elemento de imóvel encontrado na página")
            return None
        
        # Procurar por botões de navegação específicos
        botoes_proximo = driver.find_elements(By.XPATH, 
            "//a[contains(text(), 'Próxima') or contains(text(), 'Próximo') or contains(text(), '>') or contains(text(), 'Seguinte')]")
        
        # Verificar botões numéricos de paginação
        botoes_numero = driver.find_elements(By.XPATH, 
            "//a[contains(@href, 'pagina') or contains(@onclick, 'pagina') or contains(@onclick, 'proxima')]")
        
        # Verificar botões de "próxima página" por classe ou ID
        botoes_proximo_classe = driver.find_elements(By.CSS_SELECTOR, 
            ".proxima, .next, .btn-proximo, .btn-next, [class*='proxima'], [class*='next']")
        
        # Combinar todos os botões encontrados
        todos_botoes = botoes_proximo + botoes_numero + botoes_proximo_classe
        
        # Verificar se há botão válido
        for botao in todos_botoes:
            try:
                if (botao.is_displayed() and 
                    botao.is_enabled() and 
                    botao.get_attribute('href') != '#' and
                    not 'disabled' in botao.get_attribute('class', '').lower()):
                    
                    # Verificar se o botão não é o atual
                    texto_botao = botao.text.strip().lower()
                    if texto_botao not in ['1', 'atual', 'current']:
                        print(f"✅ Botão de próxima página encontrado: '{botao.text}'")
                        return botao
            except Exception as e:
                continue
        
        # Verificar se há paginação numérica ativa
        paginas_ativas = driver.find_elements(By.XPATH, 
            "//a[contains(@class, 'pagina') or contains(@class, 'page')]")
        
        for pagina in paginas_ativas:
            try:
                if (pagina.is_displayed() and 
                    pagina.is_enabled() and
                    not 'active' in pagina.get_attribute('class', '').lower() and
                    not 'current' in pagina.get_attribute('class', '').lower()):
                    
                    numero_pagina = pagina.text.strip()
                    if numero_pagina.isdigit():
                        print(f"✅ Botão de página numérica encontrado: página {numero_pagina}")
                        return pagina
            except Exception as e:
                continue
        
        print("🔍 Nenhum botão de próxima página válido encontrado")
        return None
        
    except Exception as e:
        print(f"❌ Erro ao verificar próxima página: {e}")
        return None

def buscar_imoveis_com_filtros(filtros):
    """Executa a busca de imóveis com os filtros especificados, navegando por múltiplas páginas"""
    
    driver = configurar_chromedriver()
    
    try:
        print(f"\n🚀 Iniciando busca de imóveis em {filtros['nome_cidade']}/{filtros['estado']}...")
        
        # Acessar página inicial
        driver.get(URL)
        print("Acessando página de busca...")
        
        # Aguardar página carregar completamente
        wait = WebDriverWait(driver, 20)
        
        # Aguardar e selecionar estado
        print(f"Selecionando estado: {filtros['estado']}")
        select_estado = wait.until(EC.element_to_be_clickable((By.ID, "cmb_estado")))
        select_estado = Select(select_estado)
        select_estado.select_by_value(filtros['estado'])
        print(f"✅ Estado selecionado: {filtros['estado']}")
        
        # Aguardar carregamento das cidades (pode demorar)
        print("⏳ Aguardando carregamento das cidades...")
        time.sleep(3)  # Aguardar JavaScript carregar as cidades
        
        # Aguardar e selecionar cidade
        print(f"Selecionando cidade: {filtros['nome_cidade']}")
        select_cidade = wait.until(EC.element_to_be_clickable((By.ID, "cmb_cidade")))
        select_cidade = Select(select_cidade)
        
        # Verificar se há opções de cidade
        if len(select_cidade.options) <= 1:  # Apenas "Selecione"
            print("⚠️ Cidades ainda não carregaram. Aguardando mais tempo...")
            time.sleep(5)
            # Recarregar o select
            select_cidade = Select(driver.find_element(By.ID, "cmb_cidade"))
        
        select_cidade.select_by_value(filtros['codigo_cidade'])
        
        # Verificar se a cidade foi selecionada corretamente
        cidade_selecionada = select_cidade.first_selected_option.text
        if filtros['nome_cidade'].upper() not in cidade_selecionada.upper():
            print(f"⚠️ Aviso: Selecionou '{cidade_selecionada}' em vez de '{filtros['nome_cidade']}'")
            print("   Tentando novamente...")
            time.sleep(2)
            select_cidade.select_by_value(filtros['codigo_cidade'])
            time.sleep(2)
            cidade_selecionada = select_cidade.first_selected_option.text
            print(f"   Cidade selecionada após retry: {cidade_selecionada}")
        else:
            print(f"✅ Cidade selecionada corretamente: {cidade_selecionada}")
        
        # Clicar no primeiro botão "Próximo"
        print("Clicando no botão 'Próximo'...")
        try:
            btn_next = wait.until(EC.element_to_be_clickable((By.ID, "btn_next0")))
            btn_next.click()
        except Exception as e:
            print(f"⚠️ Erro ao clicar no botão: {e}")
            driver.execute_script("document.getElementById('btn_next0').click();")
        
        time.sleep(3)
        
        # Aplicar filtros adicionais se especificados
        if filtros['tipo_imovel']:
            try:
                select_tipo = wait.until(EC.element_to_be_clickable((By.ID, "cmb_tp_imovel")))
                select_tipo = Select(select_tipo)
                select_tipo.select_by_value(filtros['tipo_imovel'])
                print(f"Tipo de imóvel: {TIPOS_IMOVEL[filtros['tipo_imovel']]}")
                time.sleep(1)
            except Exception as e:
                print(f"Erro ao selecionar tipo: {e}")
        
        if filtros['quartos']:
            try:
                select_quartos = wait.until(EC.element_to_be_clickable((By.ID, "cmb_quartos")))
                select_quartos = Select(select_quartos)
                select_quartos.select_by_value(filtros['quartos'])
                print(f"Quartos: {QUARTOS[filtros['quartos']]}")
                time.sleep(1)
            except Exception as e:
                print(f"Erro ao selecionar quartos: {e}")
        
        if filtros['faixa_valor']:
            try:
                select_valor = wait.until(EC.element_to_be_clickable((By.ID, "cmb_faixa_vlr")))
                select_valor = Select(select_valor)
                select_valor.select_by_value(filtros['faixa_valor'])
                print(f"Faixa de valor: {FAIXAS_VALOR[filtros['faixa_valor']]}")
                time.sleep(1)
            except Exception as e:
                print(f"Erro ao selecionar valor: {e}")
        
        # Clicar no segundo botão "Próximo"
        print("Clicando no segundo botão 'Próximo'...")
        try:
            btn_next2 = wait.until(EC.element_to_be_clickable((By.ID, "btn_next1")))
            btn_next2.click()
        except Exception as e:
            print(f"⚠️ Erro ao clicar no segundo botão: {e}")
            driver.execute_script("document.getElementById('btn_next1').click();")
        
        print("Aguardando carregamento dos resultados...")
        time.sleep(10)
        
        # Extrair imóveis de todas as páginas
        todos_imoveis = []
        pagina_atual = 1
        max_paginas = 20  # Aumentado o limite de segurança
        pagina_anterior = None
        tentativas_consecutivas = 0
        
        while pagina_atual <= max_paginas:
            print(f"\n📄 Processando página {pagina_atual}...")
            
            # Verificar se a página mudou
            url_atual = driver.current_url
            if url_atual == pagina_anterior:
                tentativas_consecutivas += 1
                if tentativas_consecutivas >= 2:
                    print("⚠️ Página não mudou após tentativas. Parando navegação.")
                    break
            else:
                tentativas_consecutivas = 0
                pagina_anterior = url_atual
            
            # Extrair imóveis da página atual
            imoveis_pagina = extrair_imoveis_da_pagina(driver, filtros, pagina_atual)
            
            if imoveis_pagina:
                todos_imoveis.extend(imoveis_pagina)
                print(f"✅ {len(imoveis_pagina)} imóveis encontrados na página {pagina_atual}")
            else:
                print(f"⚠️ Nenhum imóvel encontrado na página {pagina_atual}")
                # Se não há imóveis e não há botão próximo, parar
                botao_proximo = verificar_proxima_pagina(driver)
                if not botao_proximo:
                    print("🏁 Nenhum imóvel encontrado e não há próxima página")
                    break
            
            # Verificar se há próxima página
            botao_proximo = verificar_proxima_pagina(driver)
            
            if botao_proximo:
                try:
                    print(f"🔄 Navegando para página {pagina_atual + 1}...")
                    
                    # Salvar URL atual para verificar se mudou
                    url_antes = driver.current_url
                    
                    # Tentar clicar no botão
                    driver.execute_script("arguments[0].click();", botao_proximo)
                    time.sleep(5)  # Aguardar carregamento da nova página
                    
                    # Verificar se a URL mudou
                    url_depois = driver.current_url
                    if url_depois != url_antes:
                        pagina_atual += 1
                        print(f"✅ Navegação bem-sucedida para página {pagina_atual}")
                    else:
                        print("⚠️ URL não mudou após clique. Tentando novamente...")
                        time.sleep(3)
                        driver.execute_script("arguments[0].click();", botao_proximo)
                        time.sleep(5)
                        
                        if driver.current_url == url_antes:
                            print("❌ Falha na navegação. Parando.")
                            break
                        else:
                            pagina_atual += 1
                            
                except Exception as e:
                    print(f"❌ Erro ao navegar para próxima página: {e}")
                    break
            else:
                print(f"🏁 Última página alcançada (página {pagina_atual})")
                break
        
        # Salvar resultados
        if todos_imoveis:
            df = pd.DataFrame(todos_imoveis)
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            
            filename = f"imoveis_{filtros['nome_cidade'].lower()}_{timestamp}.csv"
            df.to_csv(filename, index=False, encoding='utf-8-sig')
            print(f"\n✅ Dados salvos em: {filename}")
            
            json_filename = f"imoveis_{filtros['nome_cidade'].lower()}_{timestamp}.json"
            df.to_json(json_filename, orient='records', force_ascii=False, indent=2)
            print(f"✅ Dados salvos em JSON: {json_filename}")
            
            print(f"\n🎉 Total de imóveis encontrados: {len(todos_imoveis)} em {pagina_atual} página(s)")
            
            # Mostrar resumo por página
            print("\n📊 RESUMO POR PÁGINA:")
            print("-" * 50)
            for pagina in range(1, pagina_atual + 1):
                imoveis_pagina = [im for im in todos_imoveis if im['pagina'] == pagina]
                if imoveis_pagina:
                    print(f"📄 Página {pagina}: {len(imoveis_pagina)} imóveis")
                    for imovel in imoveis_pagina[:3]:  # Mostrar apenas os 3 primeiros
                        print(f"    • {imovel['nome_imovel']} - R$ {imovel['valor']}")
                    if len(imoveis_pagina) > 3:
                        print(f"    ... e mais {len(imoveis_pagina) - 3} imóveis")
                    print()
            
            # Mostrar estatísticas
            print("\n📈 ESTATÍSTICAS:")
            print("-" * 30)
            valores = [float(im['valor'].replace('.', '').replace(',', '.')) for im in todos_imoveis if im['valor'].replace('.', '').replace(',', '.').replace('R$', '').strip().isdigit()]
            if valores:
                print(f"💰 Valor médio: R$ {sum(valores)/len(valores):,.2f}")
                print(f"💰 Valor mínimo: R$ {min(valores):,.2f}")
                print(f"💰 Valor máximo: R$ {max(valores):,.2f}")
            
        else:
            print("\n❌ Nenhum imóvel encontrado com os filtros especificados")
            
            # Salvar HTML para análise
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            html_filename = f"pagina_sem_resultados_{filtros['nome_cidade'].lower()}_{timestamp}.html"
            with open(html_filename, 'w', encoding='utf-8') as f:
                f.write(driver.page_source)
            print(f"📄 HTML salvo para análise: {html_filename}")
        
        # Salvar screenshot
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        screenshot_filename = f"screenshot_{filtros['nome_cidade'].lower()}_{timestamp}.png"
        driver.save_screenshot(screenshot_filename)
        print(f"📸 Screenshot salvo: {screenshot_filename}")
        
        return todos_imoveis
        
    except Exception as e:
        print(f"❌ Erro durante a execução: {e}")
        return []
        
    finally:
        print("Fechando navegador...")
        driver.quit()

def buscar_estados_disponiveis():
    """Busca automaticamente todos os estados disponíveis no site da Caixa"""
    print("🔍 Buscando estados disponíveis no site da Caixa...")
    
    driver = configurar_chromedriver(headless=True) # Executar sem interface gráfica para CI/CD
    
    try:
        # Acessar página inicial
        driver.get(URL)
        time.sleep(3)
        
        # Encontrar o select de estados
        select_estado = Select(driver.find_element(By.ID, "cmb_estado"))
        
        # Extrair todas as opções de estado
        estados_disponiveis = {}
        for option in select_estado.options:
            if option.get_attribute("value") and option.get_attribute("value") != "":
                sigla = option.get_attribute("value")
                nome = option.text.strip()
                estados_disponiveis[sigla] = nome
        
        print(f"✅ Encontrados {len(estados_disponiveis)} estados disponíveis:")
        for sigla, nome in estados_disponiveis.items():
            print(f"  {sigla}: {nome}")
        
        return estados_disponiveis
        
    except Exception as e:
        print(f"❌ Erro ao buscar estados: {e}")
        return {}
    finally:
        driver.quit()

def buscar_cidades_por_estado(estado_sigla):
    """Busca as cidades disponíveis para um estado específico"""
    print(f"🔍 Buscando cidades disponíveis para {estado_sigla}...")
    
    driver = configurar_chromedriver(headless=True) # Executar sem interface gráfica para CI/CD
    
    try:
        # Acessar página inicial
        driver.get(URL)
        time.sleep(3)
        
        # Selecionar estado
        select_estado = Select(driver.find_element(By.ID, "cmb_estado"))
        select_estado.select_by_value(estado_sigla)
        time.sleep(2)
        
        # Encontrar o select de cidades
        select_cidade = Select(driver.find_element(By.ID, "cmb_cidade"))
        
        # Extrair todas as opções de cidade
        cidades_disponiveis = {}
        for option in select_cidade.options:
            if option.get_attribute("value") and option.get_attribute("value") != "":
                codigo = option.get_attribute("value")
                nome = option.text.strip()
                cidades_disponiveis[codigo] = nome
        
        print(f"✅ Encontradas {len(cidades_disponiveis)} cidades para {estado_sigla}:")
        for codigo, nome in cidades_disponiveis.items():
            print(f"  {codigo}: {nome}")
        
        return cidades_disponiveis
        
    except Exception as e:
        print(f"❌ Erro ao buscar cidades para {estado_sigla}: {e}")
        return {}
    finally:
        driver.quit()

def atualizar_estados_cidades():
    """Atualiza o dicionário ESTADOS_CIDADES com dados reais do site"""
    print("🔄 Atualizando lista de estados e cidades...")
    
    # Buscar estados disponíveis
    estados_disponiveis = buscar_estados_disponiveis()
    
    if not estados_disponiveis:
        print("❌ Não foi possível buscar estados. Usando lista padrão.")
        return
    
    # Para cada estado, buscar suas cidades
    novos_estados_cidades = {}
    for sigla, nome in estados_disponiveis.items():
        print(f"\n📍 Buscando cidades para {sigla} ({nome})...")
        cidades = buscar_cidades_por_estado(sigla)
        if cidades:
            novos_estados_cidades[sigla] = cidades
    
    # Atualizar o dicionário global
    global ESTADOS_CIDADES
    ESTADOS_CIDADES = novos_estados_cidades
    
    print(f"\n✅ Atualização concluída! {len(novos_estados_cidades)} estados com suas cidades foram atualizados.")

def main():
    """Função principal"""
    print("\n" + "="*60)
    print("🏠 SCRAPER INTERATIVO - IMÓVEIS CAIXA")
    print("="*60)
    
    # Menu principal
    while True:
        print("\n📋 OPÇÕES DISPONÍVEIS:")
        print("1. 🔍 Buscar imóveis")
        print("2. 🔄 Atualizar lista de estados/cidades")
        print("3. 📊 Ver estados disponíveis")
        print("4. 🚪 Sair")
        
        opcao = input("\nEscolha uma opção (1-4): ").strip()
        
        if opcao == "1":
            # Buscar imóveis
            mostrar_menu()
            
            while True:
                # Obter entradas do usuário
                filtros = obter_entrada_usuario()
                
                # Mostrar resumo dos filtros
                print("\n" + "="*60)
                print("📋 RESUMO DOS FILTROS SELECIONADOS")
                print("="*60)
                print(f"Estado: {filtros['estado']}")
                print(f"Cidade: {filtros['nome_cidade']}")
                print(f"Tipo de Imóvel: {TIPOS_IMOVEL[filtros['tipo_imovel']]}")
                if filtros['faixa_valor']:
                    print(f"Faixa de Valor: {FAIXAS_VALOR[filtros['faixa_valor']]}")
                else:
                    print("Faixa de Valor: Indiferente")
                if filtros['quartos']:
                    print(f"Quartos: {QUARTOS[filtros['quartos']]}")
                else:
                    print("Quartos: Indiferente")
                
                # Confirmar busca
                confirmacao = input("\nDeseja executar a busca com estes filtros? (s/n): ").lower().strip()
                if confirmacao in ['s', 'sim', 'y', 'yes']:
                    break
                else:
                    print("Reiniciando configuração...")
            
            # Executar busca
            imoveis = buscar_imoveis_com_filtros(filtros)
            
            # Perguntar se quer fazer nova busca
            if imoveis:
                nova_busca = input("\nDeseja fazer uma nova busca com outros filtros? (s/n): ").lower().strip()
                if nova_busca in ['s', 'sim', 'y', 'yes']:
                    continue
                else:
                    break
            else:
                print("\nNenhum imóvel encontrado. Tente ajustar os filtros.")
                break
                
        elif opcao == "2":
            # Atualizar lista de estados/cidades
            print("\n🔄 ATUALIZANDO LISTA DE ESTADOS E CIDADES...")
            print("⚠️ Esta operação pode demorar alguns minutos...")
            
            confirmacao = input("Deseja continuar? (s/n): ").lower().strip()
            if confirmacao in ['s', 'sim', 'y', 'yes']:
                atualizar_estados_cidades()
                print("\n✅ Lista atualizada com sucesso!")
            else:
                print("Operação cancelada.")
                
        elif opcao == "3":
            # Ver estados disponíveis
            print("\n📍 ESTADOS DISPONÍVEIS:")
            print("="*60)
            for i, (sigla, cidades) in enumerate(ESTADOS_CIDADES.items(), 1):
                print(f"{i:2d}. {sigla} ({len(cidades)} cidades)")
                for codigo, nome in list(cidades.items())[:3]:  # Mostrar apenas as 3 primeiras
                    print(f"     {codigo}: {nome}")
                if len(cidades) > 3:
                    print(f"     ... e mais {len(cidades) - 3} cidades")
                print()
                
        elif opcao == "4":
            # Sair
            print("\n👋 Obrigado por usar o Scraper de Imóveis da Caixa!")
            break
            
        else:
            print("❌ Opção inválida! Tente novamente.")

if __name__ == "__main__":
    main() 