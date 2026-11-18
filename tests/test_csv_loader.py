"""Testes unitários para o módulo csv_loader."""

from pathlib import Path
import sys
from unittest.mock import MagicMock, patch

import pytest

sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "src"))

from scraper_caixa.csv_loader import (
    baixar_csv_caixa,
    buscar_imoveis_csv,
    identificar_protecao,
    carregar_csv_caixa,
    filtrar_imoveis_csv,
    parse_preco_br,
)
from scraper_caixa.exceptions import DataExtractionError

SAMPLE_CSV = """
 Lista de Imóveis da Caixa;;Data de geração:;13/11/2026;;;;;;;
 N° do imóvel;UF;Cidade;Bairro;Endereço;Preço;Valor de avaliação;Desconto;Financiamento;Descrição;Modalidade de venda;Link de acesso

 10005120 ;SC ;JOINVILLE ;AMERICA ;RUA TESTE, 100 ;150.000,00;200.000,00;25.00;Sim;Apartamento, 80.00 de área total, 70.00 de área privativa,  2 qto(s), WC, cozinha.;Venda Direta Online;https://venda-imoveis.caixa.gov.br/sistema/detalhe-imovel.asp?hdnimovel=10005120
 10005121 ;SC ;ITAJAI ;CENTRO ;RUA EXEMPLO, 200 ;320.000,00;400.000,00;20.00;Não;Casa, 120.00 de área total, 120.00 de área privativa,  3 qto(s), WC.;Leilão SFI - Edital Único;https://venda-imoveis.caixa.gov.br/sistema/detalhe-imovel.asp?hdnimovel=10005121
 10005122 ;DF ;BRASILIA ;ASA SUL ;SQS 102 ;500.000,00;600.000,00;16.67;Sim;Terreno, 0.00 de área total, 400.00 de área do terreno.;Venda Online;https://venda-imoveis.caixa.gov.br/sistema/detalhe-imovel.asp?hdnimovel=10005122
""".lstrip(
    "\n"
)


@pytest.fixture
def sample_csv_path(tmp_path: Path) -> Path:
    csv_file = tmp_path / "Lista_imoveis_geral.csv"
    csv_file.write_bytes(("\n" + SAMPLE_CSV).encode("latin1"))
    return csv_file


def test_parse_preco_br():
    assert parse_preco_br("46.497,53") == 46497.53
    assert parse_preco_br("R$ 150.000,00") == 150000.0
    assert parse_preco_br("") is None
    assert parse_preco_br("invalido") is None


def test_carregar_csv_caixa_e_data_geracao(sample_csv_path: Path):
    df, data_geracao = carregar_csv_caixa(sample_csv_path)
    assert data_geracao == "13/11/2026"
    assert len(df) == 3
    assert df.iloc[0]["id_imovel"] == "10005120"
    assert df.iloc[0]["cidade"] == "JOINVILLE"


def test_filtrar_imoveis_csv_com_acento_e_filtros(sample_csv_path: Path):
    df, _ = carregar_csv_caixa(sample_csv_path)

    # Deve casar "Itajaí" com "ITAJAI"
    itajai = filtrar_imoveis_csv(df, estado="SC", cidade="Itajaí")
    assert len(itajai) == 1
    assert itajai[0]["id_imovel"] == "10005121"
    assert itajai[0]["quartos"] == "3"
    assert itajai[0]["valor"] == "320.000,00"
    assert itajai[0]["modalidade_venda"] == "Leilão SFI - Edital Único"

    # Filtro de valor máximo
    assert filtrar_imoveis_csv(df, estado="SC", cidade="ITAJAI", valor_maximo=300000.0) == []

    # Filtro de quartos mínimo
    joinville = filtrar_imoveis_csv(df, estado="SC", cidade="JOINVILLE", quartos_minimo=2)
    assert len(joinville) == 1
    assert joinville[0]["nome_imovel"] == "Apartamento - AMERICA"


def test_buscar_imoveis_csv_config(sample_csv_path: Path):
    config = {
        "cidades": {
            "SC": {"8690": "JOINVILLE", "8676": "ITAJAI"},
            "DF": {"1809": "BRASILIA"},
        }
    }
    resultados, data_geracao = buscar_imoveis_csv(
        config, caminho_csv=sample_csv_path, baixar_se_necessario=False
    )
    assert data_geracao == "13/11/2026"
    assert len(resultados["SC"]["JOINVILLE"]) == 1
    assert len(resultados["SC"]["ITAJAI"]) == 1
    assert len(resultados["DF"]["BRASILIA"]) == 1


def test_baixar_csv_caixa_sucesso(tmp_path: Path):
    destino = tmp_path / "baixado.csv"
    mock_resp = MagicMock()
    mock_resp.status_code = 200
    mock_resp.headers = {"Content-Type": "text/csv"}
    mock_resp.iter_content.return_value = [b"\n", SAMPLE_CSV.encode("latin1")]
    mock_resp.__enter__.return_value = mock_resp
    mock_resp.__exit__.return_value = False

    with patch("scraper_caixa.csv_loader.requests.get", return_value=mock_resp) as mock_get:
        caminho = baixar_csv_caixa(destino=destino)

    mock_get.assert_called_once()
    assert caminho == destino
    assert destino.exists()
    df, data = carregar_csv_caixa(destino)
    assert len(df) == 3
    assert data == "13/11/2026"


def test_carregar_csv_invalido_levanta_erro(tmp_path: Path):
    invalido = tmp_path / "invalido.csv"
    invalido.write_text("coluna1;coluna2\n1;2\n", encoding="latin1")
    with pytest.raises(DataExtractionError):
        carregar_csv_caixa(invalido)


def _resposta_bloqueada(status: int, headers: dict, corpo: bytes) -> MagicMock:
    mock_resp = MagicMock()
    mock_resp.status_code = status
    mock_resp.reason = "Forbidden" if status == 403 else "OK"
    mock_resp.url = "https://venda-imoveis.caixa.gov.br/listaweb/Lista_imoveis_geral.csv"
    mock_resp.history = []
    mock_resp.headers = headers
    mock_resp.content = corpo
    mock_resp.__enter__.return_value = mock_resp
    mock_resp.__exit__.return_value = False
    return mock_resp


def test_baixar_csv_bloqueio_cloudflare_gera_diagnostico(tmp_path: Path, capsys):
    corpo = b"<html><head><title>Just a moment...</title></head><body>challenges.cloudflare.com</body></html>"
    resp = _resposta_bloqueada(
        403,
        {"Content-Type": "text/html; charset=UTF-8", "Server": "cloudflare", "CF-RAY": "abc123-GRU"},
        corpo,
    )
    diag = tmp_path / "resposta.html"

    with patch("scraper_caixa.csv_loader.requests.get", return_value=resp):
        with pytest.raises(DataExtractionError, match="HTTP 403, Cloudflare"):
            baixar_csv_caixa(destino=tmp_path / "x.csv", diagnostico_path=diag)

    saida = capsys.readouterr().out
    assert "Status HTTP: 403" in saida
    assert "CF-RAY: abc123-GRU" in saida
    assert "Just a moment..." in saida
    assert diag.read_bytes() == corpo
    assert not (tmp_path / "x.csv").exists()


def test_baixar_csv_html_200_sem_protecao_conhecida(tmp_path: Path, capsys):
    resp = _resposta_bloqueada(200, {"Content-Type": "text/html"}, b"<html><body>Erro</body></html>")

    with patch("scraper_caixa.csv_loader.requests.get", return_value=resp):
        with pytest.raises(DataExtractionError, match="proteção não identificada"):
            baixar_csv_caixa(destino=tmp_path / "x.csv", diagnostico_path=None)

    assert "Proteção detectada: não identificada" in capsys.readouterr().out


@pytest.mark.parametrize(
    "headers,corpo,esperado",
    [
        ({"Server": "cloudflare"}, "", "Cloudflare"),
        ({}, "<script src='https://validate.perfdrive.com/x'></script>", "Radware Bot Manager"),
        ({"Set-Cookie": "visid_incap_123=abc"}, "", "Imperva/Incapsula"),
        ({}, "<div class='h-captcha' data-sitekey='x'></div><script src='hcaptcha.com/1/api.js'>", "hCaptcha"),
    ],
)
def test_identificar_protecao(headers, corpo, esperado):
    assert esperado in identificar_protecao(headers, corpo)
