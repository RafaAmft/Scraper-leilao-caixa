#!/usr/bin/env python3
"""
Script de teste para verificar a funcionalidade de busca em todos os estados
"""

import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), 'src', 'scraper_caixa'))

try:
    from scraper import buscar_estados_disponiveis, buscar_cidades_por_estado, ESTADOS_CIDADES
except ImportError:
    print("❌ Erro: Não foi possível importar o módulo scraper")
    print("💡 Certifique-se de estar no diretório correto")
    sys.exit(1)

def testar_busca_estados():
    """Testa a busca de estados disponíveis"""
    print("🧪 TESTE DE BUSCA DE ESTADOS")
    print("="*50)
    
    # Testar busca de estados
    estados = buscar_estados_disponiveis()
    
    if estados:
        print(f"\n✅ Sucesso! Encontrados {len(estados)} estados:")
        for sigla, nome in estados.items():
            print(f"  {sigla}: {nome}")
    else:
        print("❌ Falha na busca de estados")

def testar_busca_cidades():
    """Testa a busca de cidades para alguns estados"""
    print("\n🧪 TESTE DE BUSCA DE CIDADES")
    print("="*50)
    
    # Estados para testar
    estados_teste = ["SP", "RJ", "MG", "SC"]
    
    for estado in estados_teste:
        print(f"\n📍 Testando {estado}...")
        cidades = buscar_cidades_por_estado(estado)
        
        if cidades:
            print(f"✅ {estado}: {len(cidades)} cidades encontradas")
            # Mostrar algumas cidades
            for codigo, nome in list(cidades.items())[:5]:
                print(f"  {codigo}: {nome}")
            if len(cidades) > 5:
                print(f"  ... e mais {len(cidades) - 5} cidades")
        else:
            print(f"❌ {estado}: Nenhuma cidade encontrada")

def mostrar_estados_atuais():
    """Mostra os estados atualmente configurados"""
    print("\n📊 ESTADOS ATUALMENTE CONFIGURADOS")
    print("="*50)
    
    total_estados = len(ESTADOS_CIDADES)
    total_cidades = sum(len(cidades) for cidades in ESTADOS_CIDADES.values())
    
    print(f"📈 Total de estados: {total_estados}")
    print(f"📈 Total de cidades: {total_cidades}")
    print(f"📈 Média de cidades por estado: {total_cidades/total_estados:.1f}")
    
    print("\n📍 Lista de estados:")
    for i, (sigla, cidades) in enumerate(ESTADOS_CIDADES.items(), 1):
        print(f"{i:2d}. {sigla} ({len(cidades)} cidades)")

def main():
    """Função principal de teste"""
    print("🏠 TESTE DE EXPANSÃO PARA TODOS OS ESTADOS")
    print("="*60)
    
    # Mostrar estados atuais
    mostrar_estados_atuais()
    
    # Perguntar qual teste executar
    print("\n🧪 ESCOLHA O TESTE:")
    print("1. Buscar estados disponíveis no site")
    print("2. Buscar cidades para alguns estados")
    print("3. Executar todos os testes")
    print("4. Apenas mostrar configuração atual")
    
    opcao = input("\nEscolha uma opção (1-4): ").strip()
    
    if opcao == "1":
        testar_busca_estados()
    elif opcao == "2":
        testar_busca_cidades()
    elif opcao == "3":
        testar_busca_estados()
        testar_busca_cidades()
    elif opcao == "4":
        print("✅ Configuração atual exibida acima.")
    else:
        print("❌ Opção inválida!")

if __name__ == "__main__":
    main() 