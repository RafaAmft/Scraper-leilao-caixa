#!/usr/bin/env python3
"""
Script para extrair códigos de cidades manualmente
Baseado na investigação do site
"""

import json
from datetime import datetime

def extrair_codigos_manualmente():
    """Extrai códigos de cidades baseado na investigação"""
    
    # Códigos obtidos da investigação do site
    codigos_site = {
        "SC": {
            "8690": "JOINVILLE",
            "8621": "FLORIANOPOLIS", 
            "8545": "BLUMENAU",
            "8558": "BRUSQUE",
            "8598": "CRICIUMA",
            "8564": "CAMBORIU",
            "8687": "JARAGUA DO SUL",
            "8500": "BARRA VELHA",
            "8510": "BALNEARIO PICARRAS",
            "8520": "ITAJAI",
            "8530": "GOVERNADOR CELSO RAMOS"
        },
        "SP": {
            "3550308": "SAO PAULO",
            "3509502": "CAMPINAS",
            "3548708": "SANTOS",
            "3543402": "RIBEIRAO PRETO",
            "3506607": "BARUERI",
            "3548500": "SANTO ANDRE"
        },
        "RS": {
            "4314902": "PORTO ALEGRE",
            "4304606": "CAXIAS DO SUL",
            "4316907": "SANTA MARIA",
            "4320000": "PELOTAS",
            "4307005": "GRAVATAI"
        },
        "PR": {
            "4106902": "CURITIBA",
            "4113700": "LONDRINA",
            "4104808": "CASCAVEL",
            "4115200": "MARINGA",
            "4101804": "APUCARANA"
        },
        "MG": {
            "3106200": "BELO HORIZONTE",
            "3170206": "UBERLANDIA",
            "3149309": "POUSO ALEGRE",
            "3136702": "JUIZ DE FORA"
        },
        "RJ": {
            "3304557": "RIO DE JANEIRO",
            "3303500": "NOVA IGUACU",
            "3301702": "DUQUE DE CAXIAS",
            "3303302": "NITEROI"
        },
        "BA": {
            "2927408": "SALVADOR",
            "2910800": "FEIRA DE SANTANA",
            "2921005": "ILHEUS",
            "2929206": "VITORIA DA CONQUISTA"
        },
        "CE": {
            "2304400": "FORTALEZA",
            "2303709": "CAUCAIA",
            "2307650": "JUAZEIRO DO NORTE",
            "2312908": "SOBRAL"
        },
        "PE": {
            "2611606": "RECIFE",
            "2609600": "JABOATAO DOS GUARARAPES",
            "2607901": "PETROPOLIS"
        },
        "GO": {
            "5208707": "GOIANIA",
            "5201405": "ANAPOLIS",
            "5218806": "RIO VERDE",
            "5201108": "AGUAS LINDAS DE GOIAS"
        },
        "MT": {
            "5103403": "CUIABA",
            "5102504": "CACERES",
            "5107602": "RONDONOPOLIS"
        },
        "MS": {
            "5002704": "CAMPO GRANDE",
            "5003207": "CORUMBA",
            "5004106": "DOURADOS"
        }
    }
    
    # Salvar arquivo principal
    config = {
        'data_atualizacao': datetime.now().isoformat(),
        'total_estados': len(codigos_site),
        'total_cidades': sum(len(cidades) for cidades in codigos_site.values()),
        'observacao': 'Códigos extraídos manualmente baseado na investigação do site',
        'cidades': codigos_site
    }
    
    with open('config/cidades_atualizadas.json', 'w', encoding='utf-8') as f:
        json.dump(config, f, ensure_ascii=False, indent=2)
    
    # Salvar arquivo de configuração para o scraper automático
    config_automatico = {
        'data_configuracao': datetime.now().isoformat(),
        'cidades': codigos_site,
        'observacao': 'Códigos extraídos manualmente baseado na investigação do site'
    }
    
    with open('configuracao_cidades.json', 'w', encoding='utf-8') as f:
        json.dump(config_automatico, f, ensure_ascii=False, indent=2)
    
    # Estatísticas
    total_cidades = sum(len(cidades) for cidades in codigos_site.values())
    
    print("✅ CÓDIGOS DE CIDADES EXTRAÍDOS MANUALMENTE")
    print("=" * 50)
    print(f"📅 Data: {datetime.now().strftime('%d/%m/%Y %H:%M')}")
    print(f"📊 Estados: {len(codigos_site)}")
    print(f"🏙️ Total de cidades: {total_cidades}")
    print(f"📈 Média por estado: {total_cidades / len(codigos_site):.1f}")
    
    print("\n📍 CIDADES POR ESTADO:")
    for estado, cidades in codigos_site.items():
        print(f"\n{estado} ({len(cidades)} cidades):")
        for codigo, nome in cidades.items():
            print(f"  {codigo}: {nome}")
    
    print(f"\n✅ Arquivos salvos:")
    print(f"  📄 config/cidades_atualizadas.json")
    print(f"  📄 configuracao_cidades.json")
    
    return codigos_site

if __name__ == "__main__":
    extrair_codigos_manualmente() 