"""Testes da geração do painel HTML."""

import json
from pathlib import Path
import re
import sys

import pandas as pd

sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "src"))

from scraper_caixa.csv_loader import carregar_csv_caixa
from scraper_caixa.painel import _json_para_html, gerar_painel_html, preparar_dados_painel

CSV = """ Lista de Imóveis da Caixa;;Data de geração:;13/11/2026;;;;;;;
 N° do imóvel;UF;Cidade;Bairro;Endereço;Preço;Valor de avaliação;Desconto;Financiamento;Descrição;Modalidade de venda;Link de acesso

 10005120 ;SC ;JOINVILLE ;AMERICA ;RUA TESTE, 100 ;150.000,00;200.000,00;25.00;Sim;Apartamento, 80.00 de área total, 70.00 de área privativa,  2 qto(s), WC.;Venda Direta Online;https://x/1
 10005121 ;SC ;ITAJAI ;CENTRO ;RUA </script><b>X</b> ;320.000,00;400.000,00;20.00;Não;Casa, 120.00 de área total, 0.00 de área privativa,  3 qto(s).;Leilão SFI - Edital Único;https://x/2
 10005122 ;DF ;BRASILIA ;ASA SUL ;SQS 102 ;500.000,00;600.000,00;;Sim;Terreno, 0.00 de área total, 400.00 de área do terreno.;Venda Online;https://x/3
"""
CONFIG = {"cidades": {"SC": {"8690": "JOINVILLE"}, "DF": {"1809": "Brasília"}}}


def _df(tmp_path: Path) -> pd.DataFrame:
    caminho = tmp_path / "lista.csv"
    caminho.write_bytes(CSV.encode("latin1"))
    df, _ = carregar_csv_caixa(caminho)
    return df


def test_preparar_dados_painel_colunas_e_dicionarios(tmp_path: Path):
    dados = preparar_dados_painel(_df(tmp_path), data_geracao="13/11/2026", config_cidades=CONFIG)
    col, dic = dados["col"], dados["dic"]

    assert dados["total"] == 3
    assert dados["data_lista"] == "13/11/2026"
    assert [dic["uf"][i] for i in col["uf"]] == ["SC", "SC", "DF"]
    assert [dic["tipo"][i] for i in col["tipo"]] == ["Apartamento", "Casa", "Terreno"]
    assert col["preco"] == [150000.0, 320000.0, 500000.0]
    assert col["quartos"] == [2, 3, None]
    # área privativa; se zerada, total; se ausente, terreno
    assert col["area"] == [70.0, 120.0, 400.0]
    assert col["financiamento"] == [1, 0, 1]
    # desconto ausente é calculado a partir de preço e avaliação
    assert col["desconto"][:2] == [25.0, 20.0]
    assert round(col["desconto"][2], 2) == 16.67
    # cidades monitoradas normalizadas (sem acento, maiúsculas)
    assert ["SC", "JOINVILLE"] in dados["monitoradas"]
    assert ["DF", "BRASILIA"] in dados["monitoradas"]


def test_json_para_html_nao_fecha_script():
    texto = _json_para_html({"x": "</script><script>alert(1)</script> & <!--"})
    assert "</script>" not in texto and "<" not in texto and ">" not in texto
    assert json.loads(texto)["x"] == "</script><script>alert(1)</script> & <!--"


def test_gerar_painel_html_embute_dados(tmp_path: Path):
    destino = gerar_painel_html(
        _df(tmp_path), tmp_path / "saida" / "painel.html", data_geracao="13/11/2026", config_cidades=CONFIG
    )
    html = destino.read_text(encoding="utf-8")

    assert "__DADOS_PAINEL__" not in html
    assert html.count("</script>") == 1  # só o fechamento do próprio script
    m = re.search(r"const DADOS = (\{.*?\});\n", html, re.DOTALL)
    assert m, "bloco de dados não encontrado"
    dados = json.loads(m.group(1))
    assert dados["total"] == 3
    assert dados["col"]["endereco"][1] == "RUA </script><b>X</b>"
