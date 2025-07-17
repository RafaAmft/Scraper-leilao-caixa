#!/usr/bin/env python3
"""
Script para testar o novo formato de relatório
"""

from datetime import datetime
import json

def testar_formato_relatorio():
    """Testa o novo formato de relatório"""
    
    # Simular dados de teste
    dados_teste = {
        'SC': {
            'JOINVILLE': 5,
            'BLUMENAU': 3,
            'FLORIANOPOLIS': 2
        },
        'SP': {
            'SAO PAULO': 8,
            'CAMPINAS': 4
        },
        'MS': {
            'CAMPO GRANDE': 1
        }
    }
    
    # Contar imóveis por estado
    imoveis_por_estado = {}
    for estado, cidades in dados_teste.items():
        imoveis_por_estado[estado] = sum(cidades.values())
    
    # Gerar relatório resumido (formato solicitado)
    data_atual = datetime.now().strftime("%d/%m/%Y")
    relatorio_resumido = f"Olá, hoje é dia {data_atual}, foram localizados"
    
    # Adicionar contagem por estado
    estados_com_imoveis = []
    for estado, quantidade in imoveis_por_estado.items():
        if quantidade > 0:
            estados_com_imoveis.append(f"{quantidade} imóveis em {estado}")
    
    if estados_com_imoveis:
        relatorio_resumido += " " + ", ".join(estados_com_imoveis) + "."
    else:
        relatorio_resumido += " nenhum imóvel nas cidades monitoradas."
    
    # Relatório detalhado
    relatorio_detalhado = f"""
📊 RELATÓRIO DETALHADO DE IMÓVEIS - CAIXA
Data: {datetime.now().strftime('%d/%m/%Y %H:%M')}
Total de imóveis encontrados: {sum(imoveis_por_estado.values())}

"""
    
    for estado, cidades in dados_teste.items():
        total_estado = sum(cidades.values())
        relatorio_detalhado += f"\n🏙️ {estado} ({total_estado} imóveis):\n"
        for cidade, quantidade in cidades.items():
            relatorio_detalhado += f"  • {cidade}: {quantidade} imóveis\n"
    
    relatorio_detalhado += "\n---\nRelatório gerado automaticamente"
    
    # Salvar arquivos de teste
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    
    # Salvar relatório resumido
    filename_resumido = f'teste_relatorio_resumido_{timestamp}.txt'
    with open(filename_resumido, 'w', encoding='utf-8') as f:
        f.write(relatorio_resumido)
    
    # Salvar relatório detalhado
    filename_detalhado = f'teste_relatorio_detalhado_{timestamp}.txt'
    with open(filename_detalhado, 'w', encoding='utf-8') as f:
        f.write(relatorio_detalhado)
    
    print("🧪 TESTE DO NOVO FORMATO DE RELATÓRIO")
    print("=" * 50)
    
    print(f"\n📊 DADOS DE TESTE:")
    for estado, cidades in dados_teste.items():
        total = sum(cidades.values())
        print(f"  {estado}: {total} imóveis")
        for cidade, quantidade in cidades.items():
            print(f"    • {cidade}: {quantidade}")
    
    print(f"\n📧 RELATÓRIO RESUMIDO:")
    print(f"   {relatorio_resumido}")
    
    print(f"\n📄 RELATÓRIO DETALHADO:")
    print(relatorio_detalhado)
    
    print(f"\n✅ Arquivos salvos:")
    print(f"   📄 {filename_resumido}")
    print(f"   📄 {filename_detalhado}")
    
    return relatorio_resumido, relatorio_detalhado

if __name__ == "__main__":
    testar_formato_relatorio() 