"""
Script para visualizar todas as cidades configuradas no scraper,
com destaque especial para o Distrito Federal (DF).
"""

import sys
import io

# Configurar encoding UTF-8 para Windows
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
sys.path.append('src')

from scraper_caixa.config import ESTADOS_CIDADES

def main():
    print("\n" + "="*70)
    print("CIDADES CONFIGURADAS NO SCRAPER")
    print("="*70)
    
    total_cidades = 0
    
    for estado in sorted(ESTADOS_CIDADES.keys()):
        cidades = ESTADOS_CIDADES[estado]
        num_cidades = len(cidades)
        total_cidades += num_cidades
        
        # Destaque especial para DF
        destaque = " ** NOVO!" if estado == "DF" else ""
        
        print(f"\n[{estado}] ({num_cidades} cidades){destaque}")
        print("-" * 70)
        
        for codigo, nome in sorted(cidades.items(), key=lambda x: x[1]):
            print(f"   > {nome:<30} (codigo: {codigo})")
    
    print("\n" + "="*70)
    print(f"TOTAL: {total_cidades} cidades em {len(ESTADOS_CIDADES)} estados/DF")
    print("="*70)
    
    # Destaque para o DF
    if "DF" in ESTADOS_CIDADES:
        print("\nDESTAQUE: DISTRITO FEDERAL")
        print("="*70)
        print("Regioes Administrativas Incluidas:")
        for codigo, nome in sorted(ESTADOS_CIDADES["DF"].items(), key=lambda x: x[1]):
            print(f"   > {nome} (codigo: {codigo})")
        print("\nNOTA: Codigos do DF sao internos da Caixa, NAO sao codigos IBGE!")
        print("="*70 + "\n")

if __name__ == "__main__":
    main()

