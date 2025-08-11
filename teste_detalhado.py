#!/usr/bin/env python3
"""
Script de teste detalhado que executa cada etapa separadamente
"""

import sys
import os
import time

# Adicionar o diretório src ao path
sys.path.append('src')

def testar_etapa_por_etapa():
    """Testa cada etapa do scraper separadamente"""
    try:
        from scraper_caixa.scraper import configurar_chromedriver
        from selenium.webdriver.common.by import By
        from selenium.webdriver.support.wait import WebDriverWait
        from selenium.webdriver.support.select import Select
        from selenium.webdriver.support import expected_conditions as EC
        
        print("🧪 TESTE DETALHADO ETAPA POR ETAPA")
        print("=" * 60)
        
        # Configurar driver
        print("🔧 Configurando ChromeDriver...")
        driver = configurar_chromedriver(headless=False)  # Com interface para debug
        
        try:
            # ETAPA 1: Acessar página
            print("\n📍 ETAPA 1: Acessando página...")
            driver.get("https://venda-imoveis.caixa.gov.br/sistema/busca-imovel.asp?sltTipoBusca=imoveis")
            print("✅ Página acessada com sucesso")
            
            # Aguardar página carregar
            wait = WebDriverWait(driver, 20)
            time.sleep(5)
            
            # ETAPA 2: Verificar título e URL
            print("\n📍 ETAPA 2: Verificando página...")
            titulo = driver.title
            url_atual = driver.current_url
            print(f"✅ Título: {titulo}")
            print(f"✅ URL: {url_atual}")
            
            # ETAPA 3: Aguardar e selecionar estado
            print("\n📍 ETAPA 3: Selecionando estado...")
            try:
                select_estado = wait.until(EC.element_to_be_clickable((By.ID, "cmb_estado")))
                print("✅ Elemento de estado encontrado")
                
                select_estado = Select(select_estado)
                select_estado.select_by_value("SC")
                print("✅ Estado SC selecionado")
                
                # Verificar seleção
                estado_selecionado = select_estado.first_selected_option.text
                print(f"✅ Estado selecionado: {estado_selecionado}")
                
            except Exception as e:
                print(f"❌ Erro ao selecionar estado: {e}")
                return False
            
            # ETAPA 4: Aguardar carregamento das cidades
            print("\n📍 ETAPA 4: Aguardando carregamento das cidades...")
            time.sleep(5)
            
            # Verificar se as cidades carregaram
            try:
                select_cidade = driver.find_element(By.ID, "cmb_cidade")
                select_cidade = Select(select_cidade)
                num_opcoes = len(select_cidade.options)
                print(f"✅ Campo de cidade encontrado com {num_opcoes} opções")
                
                if num_opcoes <= 1:
                    print("⚠️ Cidades ainda não carregaram. Aguardando mais...")
                    time.sleep(5)
                    select_cidade = Select(driver.find_element(By.ID, "cmb_cidade"))
                    num_opcoes = len(select_cidade.options)
                    print(f"✅ Após espera: {num_opcoes} opções")
                
            except Exception as e:
                print(f"❌ Erro ao verificar cidades: {e}")
                return False
            
            # ETAPA 5: Selecionar cidade
            print("\n📍 ETAPA 5: Selecionando cidade...")
            try:
                select_cidade.select_by_value("8690")  # JOINVILLE
                print("✅ Cidade JOINVILLE selecionada")
                
                # Verificar seleção
                cidade_selecionada = select_cidade.first_selected_option.text
                print(f"✅ Cidade selecionada: {cidade_selecionada}")
                
            except Exception as e:
                print(f"❌ Erro ao selecionar cidade: {e}")
                return False
            
            # ETAPA 6: Clicar no primeiro botão Próximo
            print("\n📍 ETAPA 6: Clicando no primeiro botão Próximo...")
            try:
                btn_next = wait.until(EC.element_to_be_clickable((By.ID, "btn_next0")))
                btn_next.click()
                print("✅ Primeiro botão Próximo clicado")
                time.sleep(3)
                
            except Exception as e:
                print(f"❌ Erro ao clicar no primeiro botão: {e}")
                print("🔄 Tentando com JavaScript...")
                try:
                    driver.execute_script("document.getElementById('btn_next0').click();")
                    print("✅ Primeiro botão Próximo clicado via JavaScript")
                    time.sleep(3)
                except Exception as e2:
                    print(f"❌ Erro também com JavaScript: {e2}")
                    return False
            
            # ETAPA 7: Verificar se chegou na próxima página
            print("\n📍 ETAPA 7: Verificando próxima página...")
            try:
                # Verificar se há campos de filtro
                campos_filtro = driver.find_elements(By.ID, "cmb_tp_imovel")
                if campos_filtro:
                    print("✅ Campos de filtro encontrados")
                else:
                    print("⚠️ Campos de filtro não encontrados")
                
                # Fazer screenshot para debug
                timestamp = time.strftime("%Y%m%d_%H%M%S")
                screenshot_path = f"debug_etapa7_{timestamp}.png"
                driver.save_screenshot(screenshot_path)
                print(f"✅ Screenshot salvo em: {screenshot_path}")
                
            except Exception as e:
                print(f"❌ Erro ao verificar próxima página: {e}")
                return False
            
            print("\n🎉 TODAS AS ETAPAS FORAM EXECUTADAS COM SUCESSO!")
            return True
            
        finally:
            driver.quit()
        
    except Exception as e:
        print(f"❌ Erro durante o teste: {e}")
        import traceback
        traceback.print_exc()
        return False

def main():
    """Função principal"""
    print("🚀 INICIANDO TESTE DETALHADO")
    print("=" * 60)
    print("⚠️ Este teste executará cada etapa separadamente")
    print("   para identificar exatamente onde está o problema.")
    
    confirmacao = input("\nDeseja continuar? (s/n): ").lower().strip()
    if confirmacao not in ['s', 'sim', 'y', 'yes']:
        print("❌ Teste cancelado pelo usuário.")
        return False
    
    try:
        resultado = testar_etapa_por_etapa()
        
        if resultado:
            print("\n🎯 RESULTADO: TESTE PASSOU!")
            print("💡 Todas as etapas funcionaram corretamente.")
        else:
            print("\n🎯 RESULTADO: TESTE FALHOU!")
            print("⚠️ Uma ou mais etapas falharam. Verifique os logs acima.")
        
        return resultado
        
    except KeyboardInterrupt:
        print("\n\n⚠️ Teste interrompido pelo usuário.")
        return False
    except Exception as e:
        print(f"\n❌ Erro inesperado: {e}")
        return False

if __name__ == "__main__":
    main() 