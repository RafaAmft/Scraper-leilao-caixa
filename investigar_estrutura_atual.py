#!/usr/bin/env python3
"""
Script para investigar a estrutura atual da página da Caixa
"""

import sys
import os
import time

# Adicionar o diretório src ao path
sys.path.append('src')

def investigar_pagina():
    """Investiga a estrutura atual da página da Caixa"""
    try:
        from scraper_caixa.scraper import configurar_chromedriver
        
        print("🔍 INVESTIGANDO ESTRUTURA DA PÁGINA DA CAIXA")
        print("=" * 60)
        
        # Configurar driver
        driver = configurar_chromedriver(headless=False)  # Com interface para debug
        
        try:
            # Acessar página inicial
            print("🌐 Acessando página da Caixa...")
            driver.get("https://venda-imoveis.caixa.gov.br/sistema/busca-imovel.asp?sltTipoBusca=imoveis")
            
            # Aguardar carregamento
            print("⏳ Aguardando carregamento da página...")
            time.sleep(10)
            
            # Verificar título da página
            titulo = driver.title
            print(f"📄 Título da página: {titulo}")
            
            # Verificar URL atual
            url_atual = driver.current_url
            print(f"🔗 URL atual: {url_atual}")
            
            # Procurar por elementos de estado
            print("\n🔍 PROCURANDO ELEMENTOS DE ESTADO...")
            
            # Tentar diferentes seletores
            seletores_estado = [
                'select[id="cmb_estado"]',
                'select[name="cmb_estado"]',
                'select[class*="estado"]',
                'select[class*="state"]',
                'select[id*="estado"]',
                'select[id*="state"]',
                'select'
            ]
            
            for seletor in seletores_estado:
                try:
                    elementos = driver.find_elements("css selector", seletor)
                    if elementos:
                        print(f"✅ Encontrado com '{seletor}': {len(elementos)} elemento(s)")
                        for i, elem in enumerate(elementos):
                            print(f"   {i+1}. ID: {elem.get_attribute('id')}")
                            print(f"      Name: {elem.get_attribute('name')}")
                            print(f"      Class: {elem.get_attribute('class')}")
                            
                            # Tentar extrair opções
                            try:
                                from selenium.webdriver.support.select import Select
                                select = Select(elem)
                                opcoes = select.options
                                print(f"      Opções: {len(opcoes)}")
                                for j, opcao in enumerate(opcoes[:5]):  # Primeiras 5
                                    valor = opcao.get_attribute('value')
                                    texto = opcao.text
                                    print(f"        {j+1}. Valor: '{valor}' | Texto: '{texto}'")
                                if len(opcoes) > 5:
                                    print(f"        ... e mais {len(opcoes) - 5} opções")
                            except Exception as e:
                                print(f"      Erro ao extrair opções: {e}")
                    else:
                        print(f"❌ Nenhum elemento encontrado com '{seletor}'")
                except Exception as e:
                    print(f"❌ Erro com seletor '{seletor}': {e}")
            
            # Procurar por elementos de cidade
            print("\n🔍 PROCURANDO ELEMENTOS DE CIDADE...")
            
            seletores_cidade = [
                'select[id="cmb_cidade"]',
                'select[name="cmb_cidade"]',
                'select[class*="cidade"]',
                'select[class*="city"]',
                'select[id*="cidade"]',
                'select[id*="city"]'
            ]
            
            for seletor in seletores_cidade:
                try:
                    elementos = driver.find_elements("css selector", seletor)
                    if elementos:
                        print(f"✅ Encontrado com '{seletor}': {len(elementos)} elemento(s)")
                        for i, elem in enumerate(elementos):
                            print(f"   {i+1}. ID: {elem.get_attribute('id')}")
                            print(f"      Name: {elem.get_attribute('name')}")
                            print(f"      Class: {elem.get_attribute('class')}")
                    else:
                        print(f"❌ Nenhum elemento encontrado com '{seletor}'")
                except Exception as e:
                    print(f"❌ Erro com seletor '{seletor}': {e}")
            
            # Verificar se há mensagens de erro ou redirecionamento
            print("\n🔍 VERIFICANDO POSSÍVEIS PROBLEMAS...")
            
            # Verificar se há mensagens de erro
            try:
                mensagens_erro = driver.find_elements("css selector", ".error, .alert, .message, .warning")
                if mensagens_erro:
                    print("⚠️ Mensagens de erro encontradas:")
                    for msg in mensagens_erro:
                        print(f"   - {msg.text}")
                else:
                    print("✅ Nenhuma mensagem de erro encontrada")
            except:
                pass
            
            # Verificar se a página foi redirecionada
            if "busca-imovel.asp" not in url_atual:
                print(f"⚠️ Página foi redirecionada para: {url_atual}")
            
            # Fazer screenshot para análise
            print("\n📸 Fazendo screenshot da página...")
            timestamp = time.strftime("%Y%m%d_%H%M%S")
            screenshot_path = f"debug_pagina_{timestamp}.png"
            driver.save_screenshot(screenshot_path)
            print(f"✅ Screenshot salvo em: {screenshot_path}")
            
            # Salvar HTML da página
            print("💾 Salvando HTML da página...")
            html_path = f"debug_pagina_{timestamp}.html"
            with open(html_path, 'w', encoding='utf-8') as f:
                f.write(driver.page_source)
            print(f"✅ HTML salvo em: {html_path}")
            
        finally:
            driver.quit()
        
        print("\n🎯 INVESTIGAÇÃO CONCLUÍDA!")
        print("💡 Verifique os arquivos gerados para análise detalhada.")
        
    except Exception as e:
        print(f"❌ Erro durante a investigação: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    investigar_pagina() 