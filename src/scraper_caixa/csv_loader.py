"""Módulo para download e filtragem da lista oficial de imóveis da Caixa (CSV)."""

from datetime import datetime
from pathlib import Path
import re
from typing import Dict, List, Optional, Tuple, Union
import unicodedata

import pandas as pd
import requests

from .exceptions import DataExtractionError
from .logger import get_logger
from .types import DadosImovel

CAIXA_CSV_URL = "https://venda-imoveis.caixa.gov.br/listaweb/Lista_imoveis_geral.csv"
DEFAULT_CSV_PATH = Path("dados_imoveis") / "Lista_imoveis_geral.csv"
DEFAULT_TIMEOUT = 60

_HEADERS = {
    "User-Agent": (
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
        "AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
    )
}

_COLUMN_MAP = {
    "n° do imovel": "id_imovel",
    "no do imovel": "id_imovel",
    "n do imovel": "id_imovel",
    "uf": "estado",
    "cidade": "cidade",
    "bairro": "bairro",
    "endereco": "endereco",
    "preco": "valor",
    "valor de avaliacao": "valor_avaliacao",
    "desconto": "desconto",
    "financiamento": "financiamento",
    "descricao": "descricao",
    "modalidade de venda": "modalidade_venda",
    "link de acesso": "link_direto",
}

_QUARTOS_RE = re.compile(r"(\d+)\s*qto\(s\)", re.IGNORECASE)
_DATA_GERACAO_RE = re.compile(r"Data de gera.{1,3}o:;\s*(\d{2}/\d{2}/\d{4})", re.IGNORECASE)


def normalizar_texto(texto: str) -> str:
    """Remove acentos, espaços extras e converte para maiúsculas."""
    if not texto:
        return ""
    sem_acento = "".join(
        ch for ch in unicodedata.normalize("NFKD", str(texto)) if not unicodedata.combining(ch)
    )
    return " ".join(sem_acento.upper().split())


def _normalizar_nome_coluna(coluna: str) -> str:
    """Normaliza nome de coluna para mapeamento tolerante a acentos e símbolos."""
    sem_acento = "".join(
        ch for ch in unicodedata.normalize("NFKD", str(coluna)) if not unicodedata.combining(ch)
    )
    # Normaliza º (U+00BA) e ° (U+00B0) para °
    sem_acento = sem_acento.replace("º", "°")
    return " ".join(sem_acento.lower().split())


def parse_preco_br(valor_str: str) -> Optional[float]:
    """Converte string monetária no padrão brasileiro ('46.497,53') para float."""
    if not valor_str:
        return None
    limpo = str(valor_str).strip().replace("R$", "").replace(" ", "")
    if not limpo:
        return None
    try:
        return float(limpo.replace(".", "").replace(",", "."))
    except ValueError:
        return None


def _extrair_quartos(descricao: str) -> Optional[str]:
    match = _QUARTOS_RE.search(descricao or "")
    return match.group(1) if match else None


def _extrair_tipo_imovel(descricao: str) -> str:
    if not descricao:
        return "Imóvel"
    return descricao.split(",", 1)[0].strip() or "Imóvel"


def baixar_csv_caixa(
    destino: Union[Path, str] = DEFAULT_CSV_PATH,
    url: str = CAIXA_CSV_URL,
    timeout: int = DEFAULT_TIMEOUT,
) -> Path:
    """Baixa o CSV oficial da Caixa para o caminho especificado e retorna o Path."""
    logger = get_logger("csv_loader")
    destino_path = Path(destino)
    destino_path.parent.mkdir(parents=True, exist_ok=True)
    temp_path = destino_path.with_suffix(".csv.tmp")

    logger.info(f"Baixando lista oficial de imóveis da Caixa: {url}")
    try:
        with requests.get(url, headers=_HEADERS, timeout=timeout, stream=True) as resp:
            resp.raise_for_status()
            content_type = resp.headers.get("Content-Type", "").lower()
            if "text/html" in content_type:
                raise DataExtractionError(
                    "O site da Caixa bloqueou o download automático (proteção anti-bot / hCaptcha). "
                    "Baixe o arquivo Lista_imoveis_geral.csv manualmente pelo navegador em "
                    "https://venda-imoveis.caixa.gov.br/sistema/download-lista.asp "
                    "e execute com: python scraper_automatico.py --csv <caminho_do_csv>"
                )
            with open(temp_path, "wb") as f:
                for chunk in resp.iter_content(chunk_size=65536):
                    if chunk:
                        f.write(chunk)
        temp_path.replace(destino_path)
    except DataExtractionError:
        if temp_path.exists():
            temp_path.unlink(missing_ok=True)
        raise
    except Exception as exc:
        if temp_path.exists():
            temp_path.unlink(missing_ok=True)
        raise DataExtractionError(f"Falha ao baixar CSV da Caixa: {exc}") from exc

    tamanho_mb = destino_path.stat().st_size / (1024 * 1024)
    logger.info(f"CSV salvo em '{destino_path}' ({tamanho_mb:.2f} MB)")
    return destino_path


def _detectar_cabecalho_e_data(caminho_csv: Path, encoding: str) -> Tuple[int, Optional[str]]:
    """Localiza a linha de cabeçalho da tabela e extrai a data de geração do CSV."""
    data_geracao: Optional[str] = None
    with open(caminho_csv, "r", encoding=encoding, errors="replace") as f:
        for idx, linha in enumerate(f):
            if idx > 15:
                break
            match_data = _DATA_GERACAO_RE.search(linha)
            if match_data:
                data_geracao = match_data.group(1)
            linha_norm = _normalizar_nome_coluna(linha)
            if ";uf;" in linha_norm and ";cidade;" in linha_norm:
                return idx, data_geracao
    raise DataExtractionError(
        f"Cabeçalho esperado não encontrado no CSV '{caminho_csv}'."
    )


def carregar_csv_caixa(
    caminho_csv: Union[Path, str],
    encoding: str = "latin1",
) -> Tuple[pd.DataFrame, Optional[str]]:
    """Carrega e normaliza o CSV da Caixa, retornando (DataFrame, data_geracao)."""
    caminho = Path(caminho_csv)
    if not caminho.exists():
        raise FileNotFoundError(f"Arquivo CSV não encontrado: {caminho}")

    header_row, data_geracao = _detectar_cabecalho_e_data(caminho, encoding)
    df = pd.read_csv(
        caminho,
        sep=";",
        skiprows=header_row,
        encoding=encoding,
        dtype=str,
    )

    renomear = {}
    for col in df.columns:
        chave = _normalizar_nome_coluna(col)
        if chave in _COLUMN_MAP:
            renomear[col] = _COLUMN_MAP[chave]
    df = df.rename(columns=renomear)

    colunas_esperadas = {"id_imovel", "estado", "cidade", "endereco", "valor"}
    faltando = colunas_esperadas - set(df.columns)
    if faltando:
        raise DataExtractionError(f"Colunas obrigatórias ausentes no CSV: {sorted(faltando)}")

    for col in df.columns:
        df[col] = df[col].fillna("").astype(str).str.strip()

    # Remover eventuais linhas vazias
    df = df[df["id_imovel"] != ""].copy()
    df["_estado_norm"] = df["estado"].map(normalizar_texto)
    df["_cidade_norm"] = df["cidade"].map(normalizar_texto)

    return df, data_geracao


def filtrar_imoveis_csv(
    df: pd.DataFrame,
    estado: str,
    cidade: str,
    tipo_imovel: Optional[str] = None,
    valor_maximo: Optional[float] = None,
    quartos_minimo: Optional[int] = None,
) -> List[DadosImovel]:
    """Filtra imóveis do DataFrame por estado, cidade e critérios opcionais."""
    estado_norm = normalizar_texto(estado)
    cidade_norm = normalizar_texto(cidade)

    filtrado = df[(df["_estado_norm"] == estado_norm) & (df["_cidade_norm"] == cidade_norm)]
    if filtrado.empty:
        return []

    agora = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    resultados: List[DadosImovel] = []

    for _, row in filtrado.iterrows():
        descricao = row.get("descricao", "")
        tipo_detectado = _extrair_tipo_imovel(descricao)
        quartos = _extrair_quartos(descricao)
        valor_str = row.get("valor", "")

        if tipo_imovel and tipo_imovel not in ("4", "Indiferente"):
            if normalizar_texto(tipo_imovel) not in normalizar_texto(tipo_detectado):
                continue

        if valor_maximo is not None:
            preco_float = parse_preco_br(valor_str)
            if preco_float is None or preco_float > valor_maximo:
                continue

        if quartos_minimo is not None:
            if not quartos or int(quartos) < quartos_minimo:
                continue

        bairro = row.get("bairro", "")
        nome_imovel = f"{tipo_detectado} - {bairro}" if bairro else tipo_detectado

        imovel: DadosImovel = {
            "id_imovel": row.get("id_imovel", ""),
            "nome_imovel": nome_imovel,
            "endereco": row.get("endereco", ""),
            "bairro": bairro or None,
            "cidade": row.get("cidade", ""),
            "estado": row.get("estado", ""),
            "valor": valor_str,
            "valor_avaliacao": row.get("valor_avaliacao") or None,
            "desconto": row.get("desconto") or None,
            "financiamento": row.get("financiamento") or None,
            "modalidade_venda": row.get("modalidade_venda") or None,
            "descricao": descricao or None,
            "quartos": quartos,
            "link_direto": row.get("link_direto") or None,
            "data_extracao": agora,
        }
        resultados.append(imovel)

    return resultados


def buscar_imoveis_csv(
    config_cidades: Dict,
    caminho_csv: Optional[Union[Path, str]] = None,
    baixar_se_necessario: bool = True,
) -> Tuple[Dict[str, Dict[str, List[DadosImovel]]], Optional[str]]:
    """Baixa/carrega o CSV da Caixa e filtra para todas as cidades configuradas."""
    destino = Path(caminho_csv) if caminho_csv else DEFAULT_CSV_PATH
    if baixar_se_necessario and caminho_csv is None:
        destino = baixar_csv_caixa(destino)

    df, data_geracao = carregar_csv_caixa(destino)

    resultados: Dict[str, Dict[str, List[DadosImovel]]] = {}
    for estado, cidades in config_cidades.get("cidades", {}).items():
        resultados[estado] = {}
        for _, nome_cidade in cidades.items():
            resultados[estado][nome_cidade] = filtrar_imoveis_csv(
                df,
                estado=estado,
                cidade=nome_cidade,
            )

    return resultados, data_geracao
