#!/usr/bin/env python3
"""
Teste muito simples para verificar se o Chrome consegue navegar
"""

import sys
import os

# Adicionar o diretório src ao path
sys.path.append('src')

def testar_navegacao_simples():
    """Testa navegação em páginas simples"""
    try:
        from scraper_caixa.scraper import configurar_chromedriver
        
        print("🧪 TESTE DE NAVEGAÇÃO SIMPLES")
        print("=" * 50)
        
        # Configurar driver
        print("🔧 Configurando ChromeDriver...")
        driver = configurar_chromedriver(headless=True)
        print("✅ Driver configurado!")
        
        # Teste 1: Página simples
        print("\n🌐 Teste 1: Página simples (httpbin)")
        driver.get("https://httpbin.org/status/200")
        print(f"✅ Página carregada: {driver.title}")
        
        # Teste 2: Google
        print("\n🌐 Teste 2: Google")
        driver.get("https://www.google.com")
        print(f"✅ Página carregada: {driver.title}")
        
        # Teste 3: Página com JavaScript
        print("\n🌐 Teste 3: Página com JavaScript")
        driver.get("https://httpbin.org/html")
        print(f"✅ Página carregada: {driver.title}")
        
        # Teste 4: Página da Caixa (apenas para ver se carrega)
        print("\n🌐 Teste 4: Página da Caixa (apenas carregamento)")
        try:
            driver.get("https://venda-imoveis.caixa.gov.br/sistema/busca-imovel.asp?sltTipoBusca=imoveis")
            print(f"✅ Página da Caixa carregada: {driver.title}")
            
            # Aguardar um pouco
            import time
            time.sleep(3)
            
            # Verificar se há elementos básicos
            from selenium.webdriver.common.by import By
            try:
                elementos = driver.find_elements(By.TAG_NAME, "body")
                print(f"✅ Elementos encontrados na página: {len(elementos)}")
            except Exception as e:
                print(f"⚠️ Erro ao buscar elementos: {e}")
                
        except Exception as e:
            print(f"❌ Erro ao carregar página da Caixa: {e}")
        
        # Fechar driver
        driver.quit()
        print("\n✅ Driver fechado com sucesso!")
        
        return True
        
    except Exception as e:
        print(f"❌ Erro durante o teste: {e}")
        import traceback
        traceback.print_exc()
        return False

def main():
    """Função principal"""
    print("🚀 INICIANDO TESTE DE NAVEGAÇÃO")
    print("=" * 50)
    
    try:
        resultado = testar_navegacao_simples()
        
        if resultado:
            print("\n🎯 RESULTADO: TESTE PASSOU!")
            print("💡 O Chrome está funcionando perfeitamente!")
        else:
            print("\n🎯 RESULTADO: TESTE FALHOU!")
            print("⚠️ Verifique os erros acima para identificar o problema.")
        
        return resultado
        
    except KeyboardInterrupt:
        print("\n❌ Teste interrompido pelo usuário.")
        return False
    except Exception as e:
        print(f"\n❌ Erro inesperado: {e}")
        return False

if __name__ == "__main__":
    main()
