"""Geração do painel HTML de imóveis da Caixa (métricas gerais + filtros).

O painel é um único arquivo HTML autossuficiente: os dados vão embutidos em
JSON (formato colunar, com dicionários para textos repetidos) e toda a
interface é HTML/CSS/JS sem dependências externas, então abre offline em
qualquer navegador.
"""

from datetime import datetime
import json
from pathlib import Path
import re
from typing import Dict, List, Optional, Tuple, Union

import pandas as pd

from .csv_loader import normalizar_texto, parse_preco_br
from .logger import get_logger

DEFAULT_PAINEL_PATH = Path("painel_imoveis.html")
_TEMPLATE_PATH = Path(__file__).parent / "templates" / "painel.html"
_MARCADOR_DADOS = "/*__DADOS_PAINEL__*/null"

_AREA_PRIVATIVA_RE = re.compile(r"([\d.,]+)\s*de\s+[áa]rea\s+privativa", re.IGNORECASE)
_AREA_TOTAL_RE = re.compile(r"([\d.,]+)\s*de\s+[áa]rea\s+total", re.IGNORECASE)
_AREA_TERRENO_RE = re.compile(r"([\d.,]+)\s*de\s+[áa]rea\s+do\s+terreno", re.IGNORECASE)
_QUARTOS_RE = re.compile(r"(\d+)\s*qto\(s\)", re.IGNORECASE)


def _numero_decimal(texto: str) -> Optional[float]:
    """Converte '80.00', '1.234,56' ou '25,5' para float."""
    if texto is None:
        return None
    s = str(texto).strip().replace("%", "")
    if not s:
        return None
    if "," in s:
        return parse_preco_br(s)
    try:
        return float(s)
    except ValueError:
        return None


def _extrair_area(descricao: str) -> Optional[float]:
    """Área privativa; se ausente, área total; se ausente, área do terreno."""
    for regex in (_AREA_PRIVATIVA_RE, _AREA_TOTAL_RE, _AREA_TERRENO_RE):
        m = regex.search(descricao or "")
        if m:
            valor = _numero_decimal(m.group(1))
            if valor:
                return round(valor, 2)
    return None


def _extrair_tipo(descricao: str) -> str:
    tipo = (descricao or "").split(",", 1)[0].strip()
    return tipo or "Não informado"


def _sim_nao(texto: str) -> Optional[int]:
    t = normalizar_texto(texto)
    if t.startswith("SIM"):
        return 1
    if t.startswith("NAO"):
        return 0
    return None


class _Dicionario:
    """Mapeia textos repetidos para índices inteiros (reduz o tamanho do JSON)."""

    def __init__(self) -> None:
        self.valores: List[str] = []
        self._indices: Dict[str, int] = {}

    def indice(self, valor: str) -> int:
        if valor not in self._indices:
            self._indices[valor] = len(self.valores)
            self.valores.append(valor)
        return self._indices[valor]


def _cidades_monitoradas(config_cidades: Optional[Dict]) -> List[Tuple[str, str]]:
    pares = []
    for uf, cidades in (config_cidades or {}).get("cidades", {}).items():
        for nome in cidades.values():
            pares.append((normalizar_texto(uf), normalizar_texto(nome)))
    return pares


def preparar_dados_painel(
    df: pd.DataFrame,
    data_geracao: Optional[str] = None,
    config_cidades: Optional[Dict] = None,
) -> Dict:
    """Converte o DataFrame do CSV da Caixa no JSON colunar consumido pelo painel."""
    dic_uf, dic_cidade, dic_bairro = _Dicionario(), _Dicionario(), _Dicionario()
    dic_modalidade, dic_tipo = _Dicionario(), _Dicionario()
    colunas: Dict[str, list] = {
        "id": [], "uf": [], "cidade": [], "bairro": [], "endereco": [],
        "preco": [], "avaliacao": [], "desconto": [], "financiamento": [],
        "modalidade": [], "tipo": [], "quartos": [], "area": [],
    }

    def valor(row, coluna: str) -> str:
        v = row.get(coluna, "")
        return "" if v is None or (isinstance(v, float) and pd.isna(v)) else str(v).strip()

    for row in df.to_dict("records"):
        descricao = valor(row, "descricao")
        preco = parse_preco_br(valor(row, "valor"))
        avaliacao = parse_preco_br(valor(row, "valor_avaliacao"))
        desconto = _numero_decimal(valor(row, "desconto"))
        if desconto is None and preco and avaliacao:
            desconto = max(0.0, (1 - preco / avaliacao) * 100)
        quartos = _QUARTOS_RE.search(descricao)

        colunas["id"].append(valor(row, "id_imovel"))
        colunas["uf"].append(dic_uf.indice(normalizar_texto(valor(row, "estado"))))
        colunas["cidade"].append(dic_cidade.indice(normalizar_texto(valor(row, "cidade"))))
        colunas["bairro"].append(dic_bairro.indice(" ".join(valor(row, "bairro").split()).upper()))
        colunas["endereco"].append(" ".join(valor(row, "endereco").split()))
        colunas["preco"].append(round(preco, 2) if preco is not None else None)
        colunas["avaliacao"].append(round(avaliacao, 2) if avaliacao is not None else None)
        colunas["desconto"].append(round(desconto, 2) if desconto is not None else None)
        colunas["financiamento"].append(_sim_nao(valor(row, "financiamento")))
        colunas["modalidade"].append(dic_modalidade.indice(valor(row, "modalidade_venda") or "Não informada"))
        colunas["tipo"].append(dic_tipo.indice(_extrair_tipo(descricao)))
        colunas["quartos"].append(int(quartos.group(1)) if quartos else None)
        colunas["area"].append(_extrair_area(descricao))

    return {
        "versao": 1,
        "gerado_em": datetime.now().strftime("%d/%m/%Y %H:%M"),
        "data_lista": data_geracao,
        "total": len(colunas["id"]),
        "monitoradas": [list(p) for p in _cidades_monitoradas(config_cidades)],
        "dic": {
            "uf": dic_uf.valores,
            "cidade": dic_cidade.valores,
            "bairro": dic_bairro.valores,
            "modalidade": dic_modalidade.valores,
            "tipo": dic_tipo.valores,
        },
        "col": colunas,
    }


def _json_para_html(dados: Dict) -> str:
    """Serializa os dados para embutir com segurança dentro de <script>."""
    texto = json.dumps(dados, ensure_ascii=False, separators=(",", ":"), allow_nan=False)
    # Impede que "</script>" (ou "<!--") em algum campo feche o bloco de script
    return texto.replace("<", "\\u003c").replace(">", "\\u003e").replace("&", "\\u0026")


def gerar_painel_html(
    df: pd.DataFrame,
    destino: Union[Path, str] = DEFAULT_PAINEL_PATH,
    data_geracao: Optional[str] = None,
    config_cidades: Optional[Dict] = None,
) -> Path:
    """Gera o painel HTML autossuficiente e retorna o caminho do arquivo."""
    logger = get_logger("painel")
    dados = preparar_dados_painel(df, data_geracao=data_geracao, config_cidades=config_cidades)
    template = _TEMPLATE_PATH.read_text(encoding="utf-8")
    if _MARCADOR_DADOS not in template:
        raise RuntimeError(f"Marcador de dados não encontrado no template {_TEMPLATE_PATH}")

    html = template.replace(_MARCADOR_DADOS, _json_para_html(dados), 1)
    destino = Path(destino)
    destino.parent.mkdir(parents=True, exist_ok=True)
    temp = destino.with_suffix(destino.suffix + ".tmp")
    temp.write_text(html, encoding="utf-8")
    temp.replace(destino)

    tamanho_mb = destino.stat().st_size / (1024 * 1024)
    logger.info(f"Painel gerado em '{destino}' ({dados['total']} imóveis, {tamanho_mb:.1f} MB)")
    return destino
