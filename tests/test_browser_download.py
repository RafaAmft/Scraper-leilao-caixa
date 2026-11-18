"""Testes unitários para o módulo browser_download."""

import os
from pathlib import Path
import sys
import time
from unittest.mock import MagicMock, patch

import pytest

sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "src"))

from scraper_caixa.browser_download import (
    baixar_csv_com_navegador,
    encontrar_csv_em_downloads,
    parece_csv_caixa,
)
from scraper_caixa.exceptions import DataExtractionError

CSV_OK = (
    " Lista de Imóveis da Caixa;;Data de geração:;13/11/2026;;\n"
    " N° do imóvel;UF;Cidade;Bairro;Endereço;Preço\n"
    " 1 ;SC ;JOINVILLE ;CENTRO ;RUA A ;100.000,00\n"
)
HTML_BLOQUEIO = "<!DOCTYPE html><html><head><title>Radware Bot Manager Block</title></head></html>"


def _escrever(caminho: Path, conteudo: str, idade_horas: float = 0) -> Path:
    caminho.write_bytes(conteudo.encode("latin1", errors="replace"))
    if idade_horas:
        instante = time.time() - idade_horas * 3600
        os.utime(caminho, (instante, instante))
    return caminho


def test_parece_csv_caixa(tmp_path: Path):
    assert parece_csv_caixa(_escrever(tmp_path / "ok.csv", CSV_OK))
    assert not parece_csv_caixa(_escrever(tmp_path / "bloqueio.csv", HTML_BLOQUEIO))
    assert not parece_csv_caixa(tmp_path / "nao_existe.csv")


def test_encontrar_csv_em_downloads_pega_o_mais_recente_valido(tmp_path: Path):
    _escrever(tmp_path / "Lista_imoveis_geral.csv", CSV_OK, idade_horas=5)
    _escrever(tmp_path / "Lista_imoveis_geral (2).csv", HTML_BLOQUEIO, idade_horas=0.1)
    recente = _escrever(tmp_path / "Lista_imoveis_geral (1).csv", CSV_OK, idade_horas=1)

    assert encontrar_csv_em_downloads(tmp_path) == recente


def test_encontrar_csv_em_downloads_ignora_arquivo_antigo(tmp_path: Path):
    _escrever(tmp_path / "Lista_imoveis_geral.csv", CSV_OK, idade_horas=48)

    assert encontrar_csv_em_downloads(tmp_path, max_idade_horas=24) is None
    assert encontrar_csv_em_downloads(tmp_path, max_idade_horas=None) is not None


def test_encontrar_csv_em_downloads_pasta_inexistente(tmp_path: Path):
    assert encontrar_csv_em_downloads(tmp_path / "nao_existe") is None


def _mock_playwright(conteudo_download: str, goto_side_effect=None):
    download = MagicMock()
    download.save_as.side_effect = lambda caminho: Path(caminho).write_bytes(conteudo_download.encode("latin1"))

    info = MagicMock()
    info.value = download
    expect_cm = MagicMock()
    expect_cm.__enter__.return_value = info
    expect_cm.__exit__.return_value = False

    pagina = MagicMock()
    pagina.expect_download.return_value = expect_cm
    if goto_side_effect is not None:
        pagina.goto.side_effect = goto_side_effect

    contexto = MagicMock()
    contexto.pages = [pagina]
    # Por padrão a requisição via contexto vem bloqueada (HTML), forçando o download pela aba
    resp_bloqueada = MagicMock(ok=True, status=200, headers={"content-type": "text/html"})
    contexto.request.get.return_value = resp_bloqueada

    playwright = MagicMock()
    playwright.chromium.launch_persistent_context.return_value = contexto
    pw_cm = MagicMock()
    pw_cm.__enter__.return_value = playwright
    pw_cm.__exit__.return_value = False
    return MagicMock(return_value=pw_cm), playwright, contexto


def test_baixar_csv_com_navegador_salva_arquivo(tmp_path: Path):
    sync_pw, playwright, contexto = _mock_playwright(CSV_OK)
    destino = tmp_path / "dados" / "lista.csv"

    with patch("scraper_caixa.browser_download._importar_playwright", return_value=sync_pw):
        caminho = baixar_csv_com_navegador(destino, perfil_dir=tmp_path / "perfil", headless=True)

    assert caminho == destino
    assert parece_csv_caixa(destino)
    kwargs = playwright.chromium.launch_persistent_context.call_args.kwargs
    assert kwargs["user_data_dir"] == str(tmp_path / "perfil")
    assert kwargs["headless"] is True
    assert kwargs["accept_downloads"] is True
    pagina = contexto.pages[0]
    assert pagina.goto.call_args.args[0].endswith("download-lista.asp")
    assert pagina.evaluate.call_args.args[1].endswith("Lista_imoveis_geral.csv")
    contexto.close.assert_called_once()


def test_baixar_csv_com_navegador_rejeita_html(tmp_path: Path):
    sync_pw, _, contexto = _mock_playwright(HTML_BLOQUEIO)
    destino = tmp_path / "lista.csv"

    with patch("scraper_caixa.browser_download._importar_playwright", return_value=sync_pw):
        with pytest.raises(DataExtractionError, match="não é o CSV"):
            baixar_csv_com_navegador(destino, perfil_dir=tmp_path / "perfil")

    assert not destino.exists()
    contexto.close.assert_called_once()


def test_baixar_csv_com_navegador_via_requisicao_com_cookies(tmp_path: Path):
    sync_pw, _, contexto = _mock_playwright(HTML_BLOQUEIO)
    contexto.request.get.return_value = MagicMock(
        ok=True, status=200, headers={"content-type": "text/csv"}, body=MagicMock(return_value=CSV_OK.encode("latin1"))
    )
    destino = tmp_path / "lista.csv"

    with patch("scraper_caixa.browser_download._importar_playwright", return_value=sync_pw):
        baixar_csv_com_navegador(destino, perfil_dir=tmp_path / "perfil", headless=True)

    assert parece_csv_caixa(destino)
    contexto.pages[0].expect_download.assert_not_called()


def test_baixar_csv_com_navegador_tenta_requisicao_de_novo_se_download_falha(tmp_path: Path):
    sync_pw, _, contexto = _mock_playwright(CSV_OK)
    pagina = contexto.pages[0]
    pagina.expect_download.return_value.__enter__.return_value.value.save_as.side_effect = Exception(
        "Target page, context or browser has been closed"
    )
    bloqueada = MagicMock(ok=True, status=200, headers={"content-type": "text/html"})
    liberada = MagicMock(
        ok=True, status=200, headers={"content-type": "text/csv"}, body=MagicMock(return_value=CSV_OK.encode("latin1"))
    )
    contexto.request.get.side_effect = [bloqueada, liberada]
    destino = tmp_path / "lista.csv"

    with patch("scraper_caixa.browser_download._importar_playwright", return_value=sync_pw):
        baixar_csv_com_navegador(destino, perfil_dir=tmp_path / "perfil", headless=True)

    assert parece_csv_caixa(destino)
    assert contexto.request.get.call_count == 2
