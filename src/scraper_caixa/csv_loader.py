"""Módulo para download e filtragem da lista oficial de imóveis da Caixa (CSV)."""

from datetime import datetime
import os
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

DIAGNOSTICO_HTML_PATH = Path("dados_imoveis") / "resposta_bloqueio.html"

# Cabeçalhos de resposta úteis para identificar CDN/WAF/anti-bot
_HEADERS_DIAGNOSTICO = (
    "Server",
    "Content-Type",
    "Content-Length",
    "Location",
    "Set-Cookie",
    "CF-RAY",
    "CF-Cache-Status",
    "CF-Mitigated",
    "X-Iinfo",
    "X-CDN",
    "X-Akamai-Transformed",
    "Akamai-GRN",
    "X-Sucuri-ID",
    "Via",
)

# (nome da proteção, marcadores procurados em cabeçalhos/corpo, em minúsculas)
_ASSINATURAS_PROTECAO = (
    ("Cloudflare", ("cf-ray", "cloudflare", "cf-chl", "challenges.cloudflare.com", "__cf_bm")),
    ("Radware Bot Manager", ("perfdrive", "radware", "shieldsquare")),
    ("Imperva/Incapsula", ("incapsula", "_incap_", "visid_incap", "x-iinfo")),
    ("Akamai", ("akamai", "_abck", "bm_sz")),
    ("F5/Shape", ("f5_cspm", "ts01", "bigipserver")),
    ("Sucuri", ("sucuri",)),
    ("hCaptcha", ("hcaptcha",)),
    ("reCAPTCHA", ("recaptcha", "google.com/recaptcha")),
)

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


def identificar_protecao(headers: Dict[str, str], corpo: str) -> List[str]:
    """Identifica CDN/WAF/anti-bot a partir dos cabeçalhos e do corpo da resposta."""
    cabecalhos = " ".join(f"{k}: {v}" for k, v in headers.items()).lower()
    texto = f"{cabecalhos}\n{(corpo or '').lower()}"
    return [nome for nome, marcadores in _ASSINATURAS_PROTECAO if any(m in texto for m in marcadores)]


def diagnosticar_resposta(resp, corpo: bytes, salvar_em: Optional[Path] = None) -> str:
    """Monta um resumo da resposta (status, cabeçalhos, proteção, trecho do corpo)."""
    texto = corpo.decode("utf-8", errors="replace")
    headers = dict(resp.headers or {})
    headers_ci = {k.lower(): v for k, v in headers.items()}

    historico = [f"{r.status_code} {r.url}" for r in (getattr(resp, "history", None) or [])]
    protecoes = identificar_protecao(headers, texto)
    titulo = re.search(r"<title[^>]*>(.*?)</title>", texto, re.IGNORECASE | re.DOTALL)
    trecho = " ".join(re.sub(r"<[^>]+>", " ", texto).split())[:500]

    linhas = [
        "🔎 DIAGNÓSTICO DO DOWNLOAD DO CSV",
        f"   URL final: {getattr(resp, 'url', '?')}",
        f"   Status HTTP: {getattr(resp, 'status_code', '?')} {getattr(resp, 'reason', '') or ''}".rstrip(),
        f"   Redirecionamentos: {' -> '.join(historico) if historico else 'nenhum'}",
        f"   Proteção detectada: {', '.join(protecoes) if protecoes else 'não identificada'}",
        f"   Título da página: {titulo.group(1).strip()[:200] if titulo else '(sem título)'}",
        f"   Tamanho do corpo: {len(corpo)} bytes",
        "   Cabeçalhos relevantes:",
    ]
    for nome in _HEADERS_DIAGNOSTICO:
        valor = headers_ci.get(nome.lower())
        if valor:
            linhas.append(f"     {nome}: {valor[:300]}")
    linhas.append(f"   Início do conteúdo (sem HTML): {trecho or '(vazio)'}")

    if salvar_em is not None:
        salvar_em = Path(salvar_em)
        salvar_em.parent.mkdir(parents=True, exist_ok=True)
        salvar_em.write_bytes(corpo)
        linhas.append(f"   Resposta completa salva em: {salvar_em}")

    return "\n".join(linhas)


def baixar_csv_caixa(
    destino: Union[Path, str] = DEFAULT_CSV_PATH,
    url: str = CAIXA_CSV_URL,
    timeout: int = DEFAULT_TIMEOUT,
    diagnostico_path: Optional[Union[Path, str]] = DIAGNOSTICO_HTML_PATH,
) -> Path:
    """Baixa o CSV oficial da Caixa para o caminho especificado e retorna o Path.

    Se a resposta não for o CSV (erro HTTP ou página HTML de bloqueio), registra um
    diagnóstico no log e salva a resposta em ``diagnostico_path`` antes de falhar.
    """
    logger = get_logger("csv_loader")
    destino_path = Path(destino)
    destino_path.parent.mkdir(parents=True, exist_ok=True)
    temp_path = destino_path.with_suffix(".csv.tmp")
    salvar_diag = Path(diagnostico_path) if diagnostico_path else None

    logger.info(f"Baixando lista oficial de imóveis da Caixa: {url}")
    try:
        with requests.get(url, headers=_HEADERS, timeout=timeout, stream=True) as resp:
            content_type = (resp.headers.get("Content-Type") or "").lower()
            bloqueado = resp.status_code >= 400 or "text/html" in content_type
            if bloqueado:
                corpo = resp.content or b""
                diagnostico = diagnosticar_resposta(resp, corpo, salvar_em=salvar_diag)
                logger.error(diagnostico)
                protecoes = identificar_protecao(dict(resp.headers or {}), corpo.decode("utf-8", "replace"))
                origem = ", ".join(protecoes) if protecoes else "proteção não identificada"
                raise DataExtractionError(
                    f"O site da Caixa não entregou o CSV (HTTP {resp.status_code}, {origem}). "
                    "Veja o diagnóstico acima. Alternativa: baixe Lista_imoveis_geral.csv pelo navegador em "
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


METODOS_DOWNLOAD = ("auto", "requests", "navegador", "downloads")


def _em_runner_hospedado_do_github() -> bool:
    """True em runners hospedados do GitHub, onde não há navegador interativo nem pasta Downloads."""
    return os.getenv("RUNNER_ENVIRONMENT") == "github-hosted"


def obter_csv_caixa(
    destino: Union[Path, str] = DEFAULT_CSV_PATH,
    metodo: str = "auto",
    perfil_navegador: Optional[Union[Path, str]] = None,
    headless: bool = False,
    pasta_downloads: Optional[Union[Path, str]] = None,
    timeout_navegador_s: Optional[int] = None,
    janela_escondida: bool = False,
) -> Path:
    """Obtém o CSV da Caixa pelo método escolhido e retorna o caminho salvo.

    Métodos:
      - ``requests``: download HTTP direto (costuma ser bloqueado pela Radware).
      - ``navegador``: Chrome real via Playwright, com perfil persistente.
      - ``downloads``: usa o CSV mais recente baixado manualmente na pasta Downloads.
      - ``auto``: tenta ``requests`` -> ``navegador`` -> ``downloads``, nessa ordem
        (em runners hospedados do GitHub, só ``requests``).
    """
    from . import browser_download as bd

    if metodo not in METODOS_DOWNLOAD:
        raise ValueError(f"Método inválido: {metodo!r}. Use um de {METODOS_DOWNLOAD}.")

    logger = get_logger("csv_loader")
    destino = Path(destino)

    if metodo == "auto":
        ordem = ["requests"] if _em_runner_hospedado_do_github() else ["requests", "navegador", "downloads"]
    else:
        ordem = [metodo]

    erros: List[str] = []
    for etapa in ordem:
        try:
            if etapa == "requests":
                return baixar_csv_caixa(destino)
            if etapa == "navegador":
                kwargs = {"headless": headless, "janela_escondida": janela_escondida}
                if perfil_navegador:
                    kwargs["perfil_dir"] = perfil_navegador
                if timeout_navegador_s:
                    kwargs["timeout_s"] = timeout_navegador_s
                return bd.baixar_csv_com_navegador(destino, **kwargs)
            if etapa == "downloads":
                encontrado = bd.encontrar_csv_em_downloads(pasta_downloads)
                if encontrado is None:
                    pasta = pasta_downloads or bd.pasta_downloads_padrao()
                    raise DataExtractionError(
                        f"Nenhum Lista_imoveis_geral*.csv recente (últimas 24h) em '{pasta}'."
                    )
                return bd.copiar_csv(encontrado, destino)
        except Exception as exc:
            erros.append(f"[{etapa}] {exc}")
            if etapa != ordem[-1]:
                logger.warning(f"Método '{etapa}' falhou; tentando o próximo. Motivo: {exc}")

    raise DataExtractionError(
        "Não foi possível obter o CSV da Caixa.\n  "
        + "\n  ".join(erros)
        + "\nAlternativa: baixe Lista_imoveis_geral.csv pelo navegador em "
        "https://venda-imoveis.caixa.gov.br/sistema/download-lista.asp e rode novamente "
        "(o script procura na pasta Downloads) ou use --csv <caminho_do_csv>."
    )


def carregar_ou_baixar_csv(
    caminho_csv: Optional[Union[Path, str]] = None,
    baixar_se_necessario: bool = True,
    metodo_download: str = "auto",
    **opcoes_download,
) -> Tuple[pd.DataFrame, Optional[str]]:
    """Obtém o CSV da Caixa (se ``caminho_csv`` não for dado) e retorna (DataFrame, data_geracao).

    ``opcoes_download`` é repassado a ``obter_csv_caixa`` (perfil_navegador,
    headless, janela_escondida, pasta_downloads, timeout_navegador_s).
    """
    destino = Path(caminho_csv) if caminho_csv else DEFAULT_CSV_PATH
    if baixar_se_necessario and caminho_csv is None:
        destino = obter_csv_caixa(destino, metodo=metodo_download, **opcoes_download)
    return carregar_csv_caixa(destino)


def filtrar_cidades_configuradas(
    df: pd.DataFrame, config_cidades: Dict
) -> Dict[str, Dict[str, List[DadosImovel]]]:
    """Filtra o DataFrame para cada cidade de ``config_cidades`` ({"cidades": {UF: {cod: nome}}})."""
    resultados: Dict[str, Dict[str, List[DadosImovel]]] = {}
    for estado, cidades in config_cidades.get("cidades", {}).items():
        resultados[estado] = {}
        for _, nome_cidade in cidades.items():
            resultados[estado][nome_cidade] = filtrar_imoveis_csv(
                df,
                estado=estado,
                cidade=nome_cidade,
            )
    return resultados


def buscar_imoveis_csv(
    config_cidades: Dict,
    caminho_csv: Optional[Union[Path, str]] = None,
    baixar_se_necessario: bool = True,
    metodo_download: str = "auto",
    **opcoes_download,
) -> Tuple[Dict[str, Dict[str, List[DadosImovel]]], Optional[str]]:
    """Obtém/carrega o CSV da Caixa e filtra para todas as cidades configuradas."""
    df, data_geracao = carregar_ou_baixar_csv(
        caminho_csv, baixar_se_necessario, metodo_download, **opcoes_download
    )
    return filtrar_cidades_configuradas(df, config_cidades), data_geracao
