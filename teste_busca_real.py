#!/usr/bin/env python3
"""
Script de teste que faz uma busca real em uma cidade para verificar o funcionamento completo
"""

import sys
import os
import time

# Adicionar o diretório src ao path
sys.path.append('src')

def testar_busca_real():
    """Testa uma busca real em uma cidade"""
    try:
        from scraper_caixa.scraper import buscar_imoveis_com_filtros
        
        print("🧪 TESTE DE BUSCA REAL")
        print("=" * 50)
        
        # Configurar filtros para teste
        filtros = {
            'estado': 'SC',
            'codigo_cidade': '8690',
            'nome_cidade': 'JOINVILLE',
            'tipo_imovel': '4',  # Indiferente
            'faixa_valor': None,  # Indiferente
            'quartos': None       # Indiferente
        }
        
        print(f"🔍 Testando busca em {filtros['nome_cidade']}/{filtros['estado']}...")
        print(f"   Código da cidade: {filtros['codigo_cidade']}")
        print(f"   Tipo de imóvel: Indiferente")
        print(f"   Faixa de valor: Indiferente")
        print(f"   Quartos: Indiferente")
        
        print("\n⏳ Iniciando busca...")
        inicio = time.time()
        
        # Executar busca
        imoveis = buscar_imoveis_com_filtros(filtros)
        
        fim = time.time()
        tempo_execucao = fim - inicio
        
        print(f"\n⏱️ Tempo de execução: {tempo_execucao:.2f} segundos")
        
        if imoveis:
            print(f"\n✅ Busca bem-sucedida! Encontrados {len(imoveis)} imóveis:")
            
            # Mostrar detalhes dos primeiros 3 imóveis
            for i, imovel in enumerate(imoveis[:3], 1):
                print(f"\n  {i}. {imovel.get('nome_imovel', 'Nome não disponível')}")
                if imovel.get('valor'):
                    print(f"     💰 R$ {imovel['valor']}")
                if imovel.get('endereco'):
                    print(f"     📍 {imovel['endereco']}")
                if imovel.get('quartos'):
                    print(f"     🛏️ {imovel['quartos']} quarto(s)")
            
            if len(imoveis) > 3:
                print(f"\n  ... e mais {len(imoveis) - 3} imóveis")
                
        else:
            print("\n⚠️ Nenhum imóvel encontrado. Isso pode ser normal se não houver ofertas ativas.")
        
        print("\n🎉 Teste de busca concluído com sucesso!")
        return True
        
    except Exception as e:
        print(f"\n❌ Erro durante o teste de busca: {e}")
        import traceback
        traceback.print_exc()
        return False

def main():
    """Função principal"""
    print("🚀 INICIANDO TESTE DE BUSCA REAL")
    print("=" * 50)
    print("⚠️ Este teste fará uma busca real no site da Caixa")
    print("   Pode demorar alguns minutos...")
    
    confirmacao = input("\nDeseja continuar? (s/n): ").lower().strip()
    if confirmacao not in ['s', 'sim', 'y', 'yes']:
        print("❌ Teste cancelado pelo usuário.")
        return False
    
    try:
        resultado = testar_busca_real()
        
        if resultado:
            print("\n🎯 RESULTADO: TESTE PASSOU!")
            print("💡 O scraper está funcionando perfeitamente!")
        else:
            print("\n🎯 RESULTADO: TESTE FALHOU!")
            print("⚠️ Verifique os erros acima para identificar o problema.")
        
        return resultado
        
    except KeyboardInterrupt:
        print("\n\n⚠️ Teste interrompido pelo usuário.")
        return False
    except Exception as e:
        print(f"\n❌ Erro inesperado: {e}")
        return False

if __name__ == "__main__":
    main() 