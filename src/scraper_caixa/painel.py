"""Geração do painel HTML de imóveis da Caixa (métricas gerais + filtros).

O painel é um único arquivo HTML autossuficiente: os dados vão embutidos em
JSON (formato colunar, com dicionários para textos repetidos) e toda a
interface é HTML/CSS/JS sem dependências externas, então abre offline em
qualquer navegador.
"""

from datetime import datetime
import json
import logging
from pathlib import Path
import re
from typing import Dict, List, Optional, Tuple, Union

import pandas as pd

from .csv_loader import normalizar_texto, parse_preco_br
from .logger import get_logger

DEFAULT_PAINEL_PATH = Path("painel_imoveis.html")
DEFAULT_HISTORICO_DIR = Path("dados_imoveis") / "historico"
MANTER_SNAPSHOTS = 10
_DADOS_RE = re.compile(r"const DADOS = (\{.*?\});\n", re.DOTALL)
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


# ---------------------------------------------------------------------------
# Histórico: compara a lista atual com a lista anterior da Caixa
# ---------------------------------------------------------------------------
# Situação de cada imóvel em relação à lista anterior
SEM_MUDANCA, NOVO, PRECO_REDUZIDO, PRECO_AUMENTADO = 0, 1, 2, 3


def _data_iso(data_lista: Optional[str]) -> str:
    """'13/11/2026' -> '2026-11-13'; sem data, usa a data de hoje."""
    try:
        return datetime.strptime((data_lista or "").strip(), "%d/%m/%Y").strftime("%Y-%m-%d")
    except ValueError:
        return datetime.now().strftime("%Y-%m-%d")


def snapshot_dos_dados(dados: Dict) -> Dict:
    """Resumo mínimo da lista para comparação futura: {id: [uf, cidade, bairro, tipo, preco]}."""
    col, dic = dados["col"], dados["dic"]
    itens = {}
    for i, id_imovel in enumerate(col["id"]):
        itens[id_imovel] = [
            dic["uf"][col["uf"][i]],
            dic["cidade"][col["cidade"][i]],
            dic["bairro"][col["bairro"][i]],
            dic["tipo"][col["tipo"][i]],
            col["preco"][i],
        ]
    return {"data_lista": dados.get("data_lista"), "data_iso": _data_iso(dados.get("data_lista")), "itens": itens}


def salvar_snapshot(snapshot: Dict, historico_dir: Union[Path, str], manter: int = MANTER_SNAPSHOTS) -> Path:
    """Grava o snapshot como lista_AAAA-MM-DD.json e mantém só os ``manter`` mais recentes."""
    historico_dir = Path(historico_dir)
    historico_dir.mkdir(parents=True, exist_ok=True)
    caminho = historico_dir / f"lista_{snapshot['data_iso']}.json"
    caminho.write_text(json.dumps(snapshot, ensure_ascii=False, separators=(",", ":")), encoding="utf-8")
    for antigo in sorted(historico_dir.glob("lista_*.json"))[:-manter]:
        antigo.unlink(missing_ok=True)
    return caminho


def carregar_snapshot_anterior(historico_dir: Union[Path, str], data_iso_atual: str) -> Optional[Dict]:
    """Retorna o snapshot mais recente com data anterior à lista atual, ou None."""
    historico_dir = Path(historico_dir)
    if not historico_dir.is_dir():
        return None
    for caminho in sorted(historico_dir.glob("lista_*.json"), reverse=True):
        if caminho.stem.replace("lista_", "") < data_iso_atual:
            try:
                return json.loads(caminho.read_text(encoding="utf-8"))
            except (OSError, ValueError):
                continue
    return None


def snapshot_de_painel_existente(caminho_html: Union[Path, str]) -> Optional[Dict]:
    """Extrai o snapshot de um painel já gerado (útil na primeira execução com histórico)."""
    caminho_html = Path(caminho_html)
    if not caminho_html.is_file():
        return None
    try:
        m = _DADOS_RE.search(caminho_html.read_text(encoding="utf-8"))
        return snapshot_dos_dados(json.loads(m.group(1))) if m else None
    except (OSError, ValueError, KeyError, IndexError, TypeError):
        return None


def comparar_com_anterior(dados: Dict, anterior: Dict) -> Dict:
    """Marca cada imóvel como novo / preço reduzido / preço aumentado e lista os que saíram."""
    itens_ant = anterior.get("itens", {})
    ids_atuais = set(dados["col"]["id"])
    situacao, preco_ant = [], []
    contagem = {"novos": 0, "preco_reduzido": 0, "preco_aumentado": 0}
    for id_imovel, preco in zip(dados["col"]["id"], dados["col"]["preco"]):
        antes = itens_ant.get(id_imovel)
        if antes is None:
            situacao.append(NOVO)
            preco_ant.append(None)
            contagem["novos"] += 1
            continue
        p_ant = antes[4]
        if preco is not None and p_ant is not None and abs(preco - p_ant) >= 0.01:
            reduziu = preco < p_ant
            situacao.append(PRECO_REDUZIDO if reduziu else PRECO_AUMENTADO)
            contagem["preco_reduzido" if reduziu else "preco_aumentado"] += 1
            preco_ant.append(p_ant)
        else:
            situacao.append(SEM_MUDANCA)
            preco_ant.append(None)

    removidos = [[id_imovel, *info] for id_imovel, info in itens_ant.items() if id_imovel not in ids_atuais]
    removidos.sort(key=lambda r: (r[1], r[2], r[3]))
    contagem["removidos"] = len(removidos)
    return {
        "data_anterior": anterior.get("data_lista") or anterior.get("data_iso"),
        "contagem": contagem,
        "situacao": situacao,
        "preco_anterior": preco_ant,
        "removidos": removidos,
    }


def aplicar_historico(
    dados: Dict,
    historico_dir: Union[Path, str],
    painel_existente: Optional[Union[Path, str]] = None,
    logger: Optional[logging.Logger] = None,
) -> None:
    """Compara com a lista anterior (se houver), grava o snapshot atual e anota ``dados['mudancas']``."""
    data_iso = _data_iso(dados.get("data_lista"))
    anterior = carregar_snapshot_anterior(historico_dir, data_iso)
    if anterior is None and painel_existente is not None:
        candidato = snapshot_de_painel_existente(painel_existente)
        if candidato and candidato["data_iso"] < data_iso:
            anterior = candidato
            salvar_snapshot(candidato, historico_dir)  # vira o ponto de partida do histórico
    if anterior is not None:
        dados["mudancas"] = comparar_com_anterior(dados, anterior)
        if logger:
            c = dados["mudancas"]["contagem"]
            logger.info(
                f"Mudanças desde a lista de {dados['mudancas']['data_anterior']}: "
                f"{c['novos']} novos, {c['removidos']} saíram, "
                f"{c['preco_reduzido']} com preço reduzido, {c['preco_aumentado']} com preço maior"
            )
    salvar_snapshot(snapshot_dos_dados(dados), historico_dir)


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
    historico_dir: Optional[Union[Path, str]] = None,
) -> Path:
    """Gera o painel HTML autossuficiente e retorna o caminho do arquivo.

    Com ``historico_dir``, compara com a lista anterior da Caixa (novos, saíram,
    preço reduzido/aumentado) e guarda um snapshot da lista atual nessa pasta.
    """
    logger = get_logger("painel")
    dados = preparar_dados_painel(df, data_geracao=data_geracao, config_cidades=config_cidades)
    if historico_dir is not None:
        try:
            aplicar_historico(dados, historico_dir, painel_existente=destino, logger=logger)
        except Exception as exc:  # o histórico é um extra: nunca impede o painel
            logger.warning(f"Não foi possível comparar com a lista anterior: {exc}")
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
