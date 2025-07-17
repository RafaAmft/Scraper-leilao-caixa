#!/usr/bin/env python3
"""
Script para testar o scraper automático com o novo formato
"""

import sys
import os

# Adicionar o diretório raiz ao path
sys.path.append('.')

def testar_scraper_automatico():
    """Testa o scraper automático com dados simulados"""
    
    print("🧪 TESTE DO SCRAPER AUTOMÁTICO")
    print("=" * 50)
    
    # Simular dados de teste
    dados_teste = {
        'SC': {
            'JOINVILLE': [
                {'nome_imovel': 'RESIDENCIAL JARDIM EUROPA', 'valor': '150.000,00'},
                {'nome_imovel': 'APARTAMENTO CENTRO', 'valor': '200.000,00'},
                {'nome_imovel': 'CASA VILA NOVA', 'valor': '180.000,00'}
            ],
            'BLUMENAU': [
                {'nome_imovel': 'CONDOMINIO GARCIA', 'valor': '220.000,00'},
                {'nome_imovel': 'APARTAMENTO VILA ITOUPAVA', 'valor': '190.000,00'}
            ]
        },
        'SP': {
            'SAO PAULO': [
                {'nome_imovel': 'APARTAMENTO VILA MADALENA', 'valor': '450.000,00'},
                {'nome_imovel': 'CASA JARDINS', 'valor': '800.000,00'},
                {'nome_imovel': 'COBERTURA ITAIM', 'valor': '1.200.000,00'}
            ],
            'CAMPINAS': [
                {'nome_imovel': 'APARTAMENTO CENTRO', 'valor': '280.000,00'},
                {'nome_imovel': 'CASA TAQUARAL', 'valor': '350.000,00'}
            ]
        },
        'MS': {
            'CAMPO GRANDE': [
                {'nome_imovel': 'APARTAMENTO CENTRO', 'valor': '180.000,00'}
            ]
        }
    }
    
    # Simular o processo do scraper automático
    relatorio_completo = []
    total_imoveis = 0
    cidades_processadas = 0
    
    print("🚀 Simulando busca automática de imóveis...")
    
    for estado, cidades in dados_teste.items():
        print(f"\n📍 Processando estado: {estado}")
        
        for nome, imoveis in cidades.items():
            cidades_processadas += 1
            
            print(f"\n🏙️ [{cidades_processadas}] Buscando em {nome}/{estado}...")
            
            if imoveis:
                relatorio_cidade = f"\n🏙️ {nome}/{estado}: {len(imoveis)} imóveis encontrados"
                
                # Mostrar os 5 primeiros imóveis
                for i, imovel in enumerate(imoveis[:5], 1):
                    relatorio_cidade += f"\n  {i}. {imovel['nome_imovel']} - R$ {imovel['valor']}"
                
                if len(imoveis) > 5:
                    relatorio_cidade += f"\n  ... e mais {len(imoveis) - 5} imóveis"
                
                relatorio_completo.append(relatorio_cidade)
                total_imoveis += len(imoveis)
            else:
                relatorio_completo.append(f"\n🏙️ {nome}/{estado}: Nenhum imóvel encontrado")
    
    # Contar imóveis por estado
    imoveis_por_estado = {}
    for estado, cidades in dados_teste.items():
        imoveis_por_estado[estado] = sum(len(imoveis) for imoveis in cidades.values())
    
    # Gerar relatório resumido (formato solicitado)
    from datetime import datetime
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
    
    # Relatório detalhado completo
    relatorio_detalhado = f"""
📊 RELATÓRIO DETALHADO DE IMÓVEIS - CAIXA
Data: {datetime.now().strftime('%d/%m/%Y %H:%M')}
Cidades processadas: {cidades_processadas}
Total de imóveis encontrados: {total_imoveis}

{''.join(relatorio_completo)}

---
Relatório gerado automaticamente
    """
    
    # Salvar relatórios em arquivos
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    
    # Salvar relatório resumido
    filename_resumido = f'teste_relatorio_resumido_{timestamp}.txt'
    with open(filename_resumido, 'w', encoding='utf-8') as f:
        f.write(relatorio_resumido)
    
    # Salvar relatório detalhado
    filename_detalhado = f'teste_relatorio_detalhado_{timestamp}.txt'
    with open(filename_detalhado, 'w', encoding='utf-8') as f:
        f.write(relatorio_detalhado)
    
    print(f"\n✅ Relatório resumido salvo em '{filename_resumido}'")
    print(f"✅ Relatório detalhado salvo em '{filename_detalhado}'")
    print(f"📊 Total de imóveis encontrados: {total_imoveis}")
    
    # Mostrar relatório resumido
    print(f"\n📧 RELATÓRIO RESUMIDO:")
    print(f"   {relatorio_resumido}")
    
    # Simular envio de email
    print("\n📧 Simulando envio de email...")
    print("   📧 Email não configurado - relatórios salvos apenas localmente")
    print("   💡 Execute 'python config/configurar_email.py' para configurar email")
    
    return relatorio_resumido

if __name__ == "__main__":
    testar_scraper_automatico() 