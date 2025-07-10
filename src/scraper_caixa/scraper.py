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

URL = "https://venda-imoveis.caixa.gov.br/sistema/busca-imovel.asp?sltTipoBusca=imoveis"

# Dicionário com estados e suas cidades disponíveis
ESTADOS_CIDADES = {
    "SC": {
        "8690": "JOINVILLE",
        "8621": "FLORIANOPOLIS", 
        "8545": "BLUMENAU",
        "8558": "BRUSQUE",
        "8598": "CRICIUMA",
        "8564": "CAMBORIU",
        "8687": "JARAGUA DO SUL"
    },
    "SP": {
        "3550308": "SAO PAULO",
        "3509502": "CAMPINAS",
        "3548708": "SANTOS",
        "3543402": "RIBEIRAO PRETO"
    },
    "RS": {
        "4314902": "PORTO ALEGRE",
        "4304606": "CAXIAS DO SUL",
        "4316907": "SANTA MARIA",
        "4320000": "PELOTAS"
    },
    "PR": {
        "4106902": "CURITIBA",
        "4113700": "LONDRINA",
        "4104808": "CASCAVEL",
        "4115200": "MARINGA"
    }
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
            
            # Extrair URL da imagem
            try:
                img_element = elemento.find_element(By.CSS_SELECTOR, "img.fotoimovel")
                url_imagem = img_element.get_attribute('src')
            except:
                url_imagem = ''
            
            return {
                'id_imovel': id_imovel,
                'cidade': cidade,
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
        # Procurar por botões de navegação
        botoes_proximo = driver.find_elements(By.XPATH, "//a[contains(text(), 'Próxima') or contains(text(), 'Próximo') or contains(text(), '>')]")
        botoes_numero = driver.find_elements(By.XPATH, "//a[contains(@href, 'pagina') or contains(@onclick, 'pagina')]")
        
        # Verificar se há botão "Próxima" ou "Próximo"
        for botao in botoes_proximo:
            if botao.is_displayed() and botao.is_enabled():
                return botao
        
        # Verificar botões numéricos (último número + 1)
        for botao in botoes_numero:
            if botao.is_displayed() and botao.is_enabled():
                return botao
        
        return None
    except Exception as e:
        print(f"Erro ao verificar próxima página: {e}")
        return None

def buscar_imoveis_com_filtros(filtros):
    """Executa a busca de imóveis com os filtros especificados, navegando por múltiplas páginas"""
    
    chrome_options = Options()
    chrome_options.add_argument("--window-size=1920,1080")
    
    service = Service(ChromeDriverManager().install())
    driver = webdriver.Chrome(service=service, options=chrome_options)
    
    try:
        print(f"\n🚀 Iniciando busca de imóveis em {filtros['nome_cidade']}/{filtros['estado']}...")
        
        # Acessar página inicial
        driver.get(URL)
        print("Acessando página de busca...")
        time.sleep(3)
        
        # Selecionar estado
        print(f"Selecionando estado: {filtros['estado']}")
        select_estado = Select(driver.find_element(By.ID, "cmb_estado"))
        select_estado.select_by_value(filtros['estado'])
        time.sleep(2)
        
        # Selecionar cidade
        print(f"Selecionando cidade: {filtros['nome_cidade']}")
        select_cidade = Select(driver.find_element(By.ID, "cmb_cidade"))
        select_cidade.select_by_value(filtros['codigo_cidade'])
        time.sleep(2)
        
        # Clicar no primeiro botão "Próximo"
        print("Clicando no botão 'Próximo'...")
        try:
            btn_next = driver.find_element(By.ID, "btn_next0")
            btn_next.click()
        except Exception as e:
            driver.execute_script("document.getElementById('btn_next0').click();")
        
        time.sleep(3)
        
        # Aplicar filtros adicionais se especificados
        if filtros['tipo_imovel']:
            try:
                select_tipo = Select(driver.find_element(By.ID, "cmb_tp_imovel"))
                select_tipo.select_by_value(filtros['tipo_imovel'])
                print(f"Tipo de imóvel: {TIPOS_IMOVEL[filtros['tipo_imovel']]}")
                time.sleep(1)
            except Exception as e:
                print(f"Erro ao selecionar tipo: {e}")
        
        if filtros['quartos']:
            try:
                select_quartos = Select(driver.find_element(By.ID, "cmb_quartos"))
                select_quartos.select_by_value(filtros['quartos'])
                print(f"Quartos: {QUARTOS[filtros['quartos']]}")
                time.sleep(1)
            except Exception as e:
                print(f"Erro ao selecionar quartos: {e}")
        
        if filtros['faixa_valor']:
            try:
                select_valor = Select(driver.find_element(By.ID, "cmb_faixa_vlr"))
                select_valor.select_by_value(filtros['faixa_valor'])
                print(f"Faixa de valor: {FAIXAS_VALOR[filtros['faixa_valor']]}")
                time.sleep(1)
            except Exception as e:
                print(f"Erro ao selecionar valor: {e}")
        
        # Clicar no segundo botão "Próximo"
        print("Clicando no segundo botão 'Próximo'...")
        try:
            btn_next2 = driver.find_element(By.ID, "btn_next1")
            btn_next2.click()
        except Exception as e:
            driver.execute_script("document.getElementById('btn_next1').click();")
        
        print("Aguardando carregamento dos resultados...")
        time.sleep(10)
        
        # Extrair imóveis de todas as páginas
        todos_imoveis = []
        pagina_atual = 1
        max_paginas = 10  # Limite de segurança
        
        while pagina_atual <= max_paginas:
            print(f"\n📄 Processando página {pagina_atual}...")
            
            # Extrair imóveis da página atual
            imoveis_pagina = extrair_imoveis_da_pagina(driver, filtros, pagina_atual)
            
            if imoveis_pagina:
                todos_imoveis.extend(imoveis_pagina)
                print(f"✅ {len(imoveis_pagina)} imóveis encontrados na página {pagina_atual}")
            else:
                print(f"⚠️ Nenhum imóvel encontrado na página {pagina_atual}")
            
            # Verificar se há próxima página
            botao_proximo = verificar_proxima_pagina(driver)
            
            if botao_proximo:
                try:
                    print(f"🔄 Navegando para página {pagina_atual + 1}...")
                    driver.execute_script("arguments[0].click();", botao_proximo)
                    time.sleep(5)  # Aguardar carregamento da nova página
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

def main():
    """Função principal"""
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
            main()
    else:
        print("\nNenhum imóvel encontrado. Tente ajustar os filtros.")

if __name__ == "__main__":
    main() 