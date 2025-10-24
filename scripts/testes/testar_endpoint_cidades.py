#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Script para testar o endpoint de cidades da Caixa
"""

import requests
import json
from datetime import datetime

def testar_endpoint_cidades():
    """Testa o endpoint de cidades da Caixa"""
    
    url = "https://venda-imoveis.caixa.gov.br/sistema/carregaListaCidades.asp"
    
    print("🔍 Testando endpoint de cidades da Caixa...")
    print(f"URL: {url}")
    print("="*50)
    
    try:
        # Testar sem parâmetros primeiro
        print("\n📡 Testando sem parâmetros...")
        response = requests.get(url, timeout=30)
        
        print(f"Status Code: {response.status_code}")
        print(f"Content-Type: {response.headers.get('content-type', 'N/A')}")
        print(f"Tamanho da resposta: {len(response.content)} bytes")
        
        # Mostrar primeiros 500 caracteres da resposta
        print(f"\n📄 Primeiros 500 caracteres da resposta:")
        print("-" * 50)
        print(response.text[:500])
        print("-" * 50)
        
        # Testar com diferentes parâmetros
        parametros_teste = [
            {"estado": "SC"},
            {"uf": "SC"},
            {"codigo_estado": "SC"},
            {"estado": "SC", "uf": "SC"},
            {"estado": "42"},  # Código IBGE de SC
            {"uf": "42"}
        ]
        
        for i, params in enumerate(parametros_teste, 1):
            print(f"\n🔍 Teste {i}: {params}")
            try:
                response = requests.get(url, params=params, timeout=30)
                print(f"  Status: {response.status_code}")
                print(f"  URL completa: {response.url}")
                
                if response.status_code == 200:
                    print(f"  Tamanho: {len(response.content)} bytes")
                    print(f"  Primeiros 200 chars: {response.text[:200]}")
                    
                    # Tentar parsear como JSON
                    try:
                        data = response.json()
                        print(f"  ✅ Resposta é JSON válido!")
                        print(f"  Estrutura: {type(data)}")
                        if isinstance(data, list):
                            print(f"  Número de itens: {len(data)}")
                            if data:
                                print(f"  Primeiro item: {data[0]}")
                        elif isinstance(data, dict):
                            print(f"  Chaves: {list(data.keys())}")
                    except:
                        print(f"  ❌ Não é JSON válido")
                        
                        # Tentar parsear como HTML
                        if "<" in response.text and ">" in response.text:
                            print(f"  🏷️ Parece ser HTML")
                        else:
                            print(f"  📝 Texto simples")
                
            except Exception as e:
                print(f"  ❌ Erro: {e}")
        
        # Testar com diferentes estados
        estados = ["SC", "MS", "SP"]
        for estado in estados:
            print(f"\n📍 Testando estado: {estado}")
            try:
                response = requests.get(url, params={"estado": estado}, timeout=30)
                print(f"  Status: {response.status_code}")
                
                if response.status_code == 200:
                    print(f"  Tamanho: {len(response.content)} bytes")
                    
                    # Salvar resposta para análise
                    filename = f"resposta_cidades_{estado}.txt"
                    with open(filename, "w", encoding="utf-8") as f:
                        f.write(response.text)
                    print(f"  💾 Resposta salva em: {filename}")
                    
            except Exception as e:
                print(f"  ❌ Erro: {e}")
        
        print(f"\n✅ Teste concluído!")
        
    except Exception as e:
        print(f"❌ Erro geral: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    testar_endpoint_cidades() 