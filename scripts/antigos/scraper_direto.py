#!/usr/bin/env python3
"""
Scraper que roda diretamente sem perguntas
"""

import time
from datetime import datetime
import json
import sys

# Adicionar o diretório src ao path
sys.path.append('src')

from scraper_caixa.scraper import buscar_imoveis_com_filtros

# Cidades com códigos conhecidos (vou usar os que já temos)
CIDADES_CONFIGURADAS = {
    'SC': {
        '8690': 'JOINVILLE',
        '8545': 'BLUMENAU',
        '8500': 'BARRA VELHA',
        '8510': 'BALNEARIO PICARRAS',
        '8520': 'ITAJAI',
        '8530': 'GOVERNADOR CELSO RAMOS'
    },
    'MS': {
        '5002704': 'CAMPO GRANDE'
    },
    'SP': {
        '3550308': 'SAO PAULO',
        '3550000': 'SAO JOSE DO RIO PRETO',
        '3550100': 'BADY BASSIT'
    }
}

def buscar_todas_cidades():
    """Busca imóveis em todas as cidades configuradas"""
    print("🚀 INICIANDO SCRAPER AUTOMÁTICO")
    print("="*50)
    print(f"📅 Data: {datetime.now().strftime('%d/%m/%Y %H:%M')}")
    
    relatorio_completo = []
    total_imoveis = 0
    cidades_processadas = 0
    
    for estado, cidades in CIDADES_CONFIGURADAS.items():
        print(f"\n📍 Processando {estado}...")
        
        for codigo, nome in cidades.items():
            cidades_processadas += 1
            print(f"\n🏙️ [{cidades_processadas}] {nome}/{estado}...")
            
            # Configurar filtros
            filtros = {
                'estado': estado,
                'codigo_cidade': codigo,
                'nome_cidade': nome,
                'tipo_imovel': '4',  # Indiferente
                'faixa_valor': None,  # Indiferente
                'quartos': None       # Indiferente
            }
            
            try:
                imoveis = buscar_imoveis_com_filtros(filtros)
                
                if imoveis:
                    relatorio_cidade = f"\n🏙️ {nome}/{estado}: {len(imoveis)} imóveis"
                    
                    # Mostrar os 3 primeiros imóveis
                    for i, imovel in enumerate(imoveis[:3], 1):
                        relatorio_cidade += f"\n  {i}. {imovel['nome_imovel']} - R$ {imovel['valor']}"
                    
                    if len(imoveis) > 3:
                        relatorio_cidade += f"\n  ... e mais {len(imoveis) - 3} imóveis"
                    
                    relatorio_completo.append(relatorio_cidade)
                    total_imoveis += len(imoveis)
                else:
                    relatorio_completo.append(f"\n🏙️ {nome}/{estado}: Nenhum imóvel encontrado")
                
                time.sleep(2)  # Pausa entre buscas
                
            except Exception as e:
                relatorio_completo.append(f"\n❌ {nome}/{estado}: Erro - {e}")
                print(f"❌ Erro em {nome}: {e}")
    
    # Criar relatório final
    relatorio_final = f"""
📊 RELATÓRIO DE IMÓVEIS - CAIXA
Data: {datetime.now().strftime('%d/%m/%Y %H:%M')}
Cidades processadas: {cidades_processadas}
Total de imóveis encontrados: {total_imoveis}

{''.join(relatorio_completo)}

---
Relatório gerado automaticamente
    """
    
    # Salvar relatório
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename_relatorio = f'relatorio_{timestamp}.txt'
    with open(filename_relatorio, 'w', encoding='utf-8') as f:
        f.write(relatorio_final)
    
    print(f"\n✅ Relatório salvo: {filename_relatorio}")
    print(f"📊 Total de imóveis: {total_imoveis}")
    
    return relatorio_final

if __name__ == "__main__":
    buscar_todas_cidades() 