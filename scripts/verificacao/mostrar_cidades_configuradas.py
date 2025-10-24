#!/usr/bin/env python3
"""
Script para mostrar as cidades configuradas atualmente
"""

import json
from datetime import datetime

def carregar_configuracao():
    """Carrega configuração das cidades"""
    try:
        with open('configuracao_cidades.json', 'r', encoding='utf-8') as f:
            return json.load(f)
    except FileNotFoundError:
        print("❌ Arquivo de configuração não encontrado!")
        return None

def main():
    """Função principal"""
    print("🏙️ CIDADES CONFIGURADAS NO SCRAPER")
    print("=" * 50)
    
    config = carregar_configuracao()
    if not config:
        return
    
    print(f"📅 Data da configuração: {config['data_configuracao']}")
    print(f"📝 Observação: {config['observacao']}")
    
    total_cidades = 0
    
    for estado, cidades in config['cidades'].items():
        print(f"\n📍 {estado}:")
        for codigo, nome in cidades.items():
            print(f"   • {nome} (código: {codigo})")
            total_cidades += 1
    
    print(f"\n📊 Total de cidades configuradas: {total_cidades}")
    
    print("\n" + "=" * 50)
    print("🔧 PRÓXIMOS PASSOS:")
    print("=" * 50)
    print("1. Para verificar se os códigos estão corretos:")
    print("   python verificar_codigos_cidades.py")
    print("\n2. Para executar o scraper automático:")
    print("   python scraper_automatico.py")
    print("\n3. Para executar o scraper interativo:")
    print("   python src/scraper_caixa/scraper.py")

if __name__ == "__main__":
    main() 