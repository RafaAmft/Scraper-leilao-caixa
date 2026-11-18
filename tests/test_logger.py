"""Testes do logger do pacote (sem linhas duplicadas no console)."""

import io
import logging
from pathlib import Path
import sys

sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "src"))

from scraper_caixa.logger import _SemDuplicarNoConsole


def _registro() -> logging.LogRecord:
    return logging.LogRecord("csv_loader", logging.INFO, __file__, 1, "msg", None, None)


def test_filtro_silencia_quando_raiz_escreve_no_console(monkeypatch):
    raiz = logging.getLogger()
    handler = logging.StreamHandler(sys.stderr)
    monkeypatch.setattr(raiz, "handlers", [handler])

    assert _SemDuplicarNoConsole().filter(_registro()) is False


def test_filtro_libera_quando_raiz_so_tem_arquivo_ou_nada(monkeypatch, tmp_path):
    raiz = logging.getLogger()
    filtro = _SemDuplicarNoConsole()

    monkeypatch.setattr(raiz, "handlers", [])
    assert filtro.filter(_registro()) is True

    arquivo = logging.FileHandler(tmp_path / "x.log", encoding="utf-8")
    try:
        monkeypatch.setattr(raiz, "handlers", [arquivo, logging.StreamHandler(io.StringIO())])
        assert filtro.filter(_registro()) is True
    finally:
        arquivo.close()
