#!/usr/bin/env python3
"""
Script de teste local para verificar se o scraper está funcionando
"""

import sys
import os

# Adicionar o diretório src ao path
sys.path.append('src')

def testar_importacao():
    """Testa se consegue importar o módulo do scraper"""
    try:
        from scraper_caixa.scraper import configurar_chromedriver
        print("✅ Importação do módulo scraper bem-sucedida!")
        return True
    except Exception as e:
        print(f"❌ Erro ao importar módulo scraper: {e}")
        return False

def testar_chromedriver():
    """Testa se consegue configurar o ChromeDriver"""
    try:
        from scraper_caixa.scraper import configurar_chromedriver
        print("🔧 Testando configuração do ChromeDriver...")
        
        driver = configurar_chromedriver(headless=True)
        print("✅ ChromeDriver configurado com sucesso!")
        
        # Testar acesso a uma página simples
        driver.get("https://www.google.com")
        print("✅ Acesso à internet funcionando!")
        
        driver.quit()
        print("✅ Driver fechado com sucesso!")
        return True
        
    except Exception as e:
        print(f"❌ Erro ao configurar ChromeDriver: {e}")
        return False

def testar_configuracao_cidades():
    """Testa se consegue carregar a configuração das cidades"""
    try:
        import json
        
        with open('configuracao_cidades.json', 'r', encoding='utf-8') as f:
            config = json.load(f)
        
        print("✅ Configuração de cidades carregada com sucesso!")
        print(f"   Estados configurados: {list(config['cidades'].keys())}")
        
        total_cidades = sum(len(cidades) for cidades in config['cidades'].values())
        print(f"   Total de cidades: {total_cidades}")
        
        return True
        
    except Exception as e:
        print(f"❌ Erro ao carregar configuração de cidades: {e}")
        return False

def main():
    """Função principal de teste"""
    print("🧪 TESTE LOCAL DO SCRAPER")
    print("=" * 40)
    
    testes = [
        ("Importação do módulo", testar_importacao),
        ("Configuração do ChromeDriver", testar_chromedriver),
        ("Configuração de cidades", testar_configuracao_cidades)
    ]
    
    resultados = []
    
    for nome_teste, funcao_teste in testes:
        print(f"\n🔍 {nome_teste}...")
        try:
            resultado = funcao_teste()
            resultados.append((nome_teste, resultado))
        except Exception as e:
            print(f"❌ Erro inesperado no teste: {e}")
            resultados.append((nome_teste, False))
    
    print("\n" + "=" * 40)
    print("📊 RESUMO DOS TESTES")
    print("=" * 40)
    
    sucessos = 0
    for nome_teste, resultado in resultados:
        status = "✅ PASSOU" if resultado else "❌ FALHOU"
        print(f"{nome_teste}: {status}")
        if resultado:
            sucessos += 1
    
    print(f"\n🎯 Resultado: {sucessos}/{len(resultados)} testes passaram")
    
    if sucessos == len(resultados):
        print("🎉 Todos os testes passaram! O scraper está funcionando localmente.")
        print("💡 Agora você pode testar no CI/CD ou executar o scraper completo.")
    else:
        print("⚠️ Alguns testes falharam. Verifique os erros acima antes de continuar.")
    
    return sucessos == len(resultados)

if __name__ == "__main__":
    main() 