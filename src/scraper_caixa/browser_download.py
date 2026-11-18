"""Download do CSV da Caixa por navegador real (Playwright) e busca na pasta Downloads.

O site da Caixa usa o Radware Bot Manager, que bloqueia requisições simples
(``requests``) e exige um navegador real executando JavaScript (às vezes com
hCaptcha). Este módulo oferece duas alternativas:

1. ``baixar_csv_com_navegador``: abre o Chrome via Playwright com um perfil
   persistente. Na primeira vez, se aparecer o captcha, o usuário resolve na
   janela; os cookies de liberação da Radware ficam salvos no perfil e são
   reaproveitados nas execuções seguintes.
2. ``encontrar_csv_em_downloads``: localiza o ``Lista_imoveis_geral*.csv`` mais
   recente baixado manualmente pelo navegador do usuário.
"""

from datetime import datetime, timedelta
from pathlib import Path
import shutil
from typing import Optional, Union

from .exceptions import DataExtractionError
from .logger import get_logger

CAIXA_CSV_URL = "https://venda-imoveis.caixa.gov.br/listaweb/Lista_imoveis_geral.csv"
CAIXA_PAGINA_DOWNLOAD_URL = "https://venda-imoveis.caixa.gov.br/sistema/download-lista.asp"
DEFAULT_PERFIL_DIR = Path("navegador_perfil")
DEFAULT_TIMEOUT_S = 180
PADRAO_ARQUIVO_CSV = "Lista_imoveis_geral*.csv"


def pasta_downloads_padrao() -> Path:
    """Retorna a pasta Downloads do usuário (Windows, Linux e macOS)."""
    return Path.home() / "Downloads"


def parece_csv_caixa(caminho: Union[Path, str]) -> bool:
    """Confere se o arquivo é o CSV da Caixa e não uma página HTML de bloqueio."""
    caminho = Path(caminho)
    if not caminho.exists() or caminho.stat().st_size == 0:
        return False
    with open(caminho, "rb") as f:
        inicio = f.read(4096)
    texto = inicio.decode("latin1", errors="replace").lower()
    if texto.lstrip().startswith("<") or "<html" in texto:
        return False
    return ";" in texto and "uf" in texto


def _importar_playwright():
    try:
        from playwright.sync_api import sync_playwright
    except ImportError as exc:
        raise ImportError(
            "Playwright não instalado. Execute: pip install playwright && playwright install chromium"
        ) from exc
    return sync_playwright


def _abrir_contexto(playwright, perfil_dir: Path, headless: bool):
    """Abre contexto persistente, preferindo o Google Chrome instalado."""
    logger = get_logger("browser_download")
    opcoes = dict(
        user_data_dir=str(perfil_dir),
        headless=headless,
        accept_downloads=True,
        viewport={"width": 1280, "height": 900},
        locale="pt-BR",
    )
    try:
        return playwright.chromium.launch_persistent_context(channel="chrome", **opcoes)
    except Exception as exc:  # Chrome não instalado: usa o Chromium do Playwright
        logger.info(f"Google Chrome indisponível ({exc.__class__.__name__}); usando Chromium do Playwright.")
        return playwright.chromium.launch_persistent_context(**opcoes)


def baixar_csv_com_navegador(
    destino: Union[Path, str],
    perfil_dir: Union[Path, str] = DEFAULT_PERFIL_DIR,
    headless: bool = False,
    timeout_s: int = DEFAULT_TIMEOUT_S,
    url: str = CAIXA_CSV_URL,
    pagina_inicial: Optional[str] = CAIXA_PAGINA_DOWNLOAD_URL,
) -> Path:
    """Baixa o CSV da Caixa com um navegador real e salva em ``destino``.

    Fluxo:
      1. Abre ``pagina_inicial`` (página de download da Caixa) no perfil persistente,
         o que deixa o navegador passar pela verificação JavaScript da Radware.
      2. Pede o CSV pela API de requisições do Playwright, que reaproveita os cookies
         do navegador (sem depender do mecanismo de download do Chromium).
      3. Se ainda vier bloqueado, navega até o CSV na própria aba: com
         ``headless=False``, resolva o captcha na janela e o download começa sozinho.
         O script espera até ``timeout_s`` segundos e, se o download do navegador
         falhar, tenta a requisição do passo 2 mais uma vez (já com os novos cookies).
    """
    logger = get_logger("browser_download")
    sync_playwright = _importar_playwright()
    destino = Path(destino)
    destino.parent.mkdir(parents=True, exist_ok=True)
    perfil_dir = Path(perfil_dir)
    perfil_dir.mkdir(parents=True, exist_ok=True)
    temp = destino.with_suffix(".csv.tmp")
    temp.unlink(missing_ok=True)

    logger.info(
        f"Baixando CSV pelo navegador (perfil '{perfil_dir}', headless={headless}). "
        + ("" if headless else f"Se aparecer um captcha, resolva-o na janela (até {timeout_s}s).")
    )

    with sync_playwright() as p:
        contexto = _abrir_contexto(p, perfil_dir, headless)
        try:
            pagina = contexto.pages[0] if contexto.pages else contexto.new_page()
            if pagina_inicial:
                try:
                    pagina.goto(pagina_inicial, wait_until="domcontentloaded", timeout=60_000)
                except Exception as exc:
                    logger.warning(f"Falha ao abrir a página inicial ({exc.__class__.__name__}); seguindo para o CSV.")

            if _baixar_via_requisicao(contexto, url, temp, referer=pagina_inicial):
                logger.info("CSV obtido via requisição com os cookies do navegador.")
            else:
                erro_navegacao: Optional[Exception] = None
                try:
                    with pagina.expect_download(timeout=timeout_s * 1000) as info_download:
                        # Navega a partir da página já aberta. Se a Radware interceptar,
                        # a aba mostra o desafio; após resolvê-lo, ela redireciona ao CSV.
                        pagina.evaluate("u => { window.location.href = u; }", url)
                    info_download.value.save_as(str(temp))
                except Exception as exc:
                    erro_navegacao = exc

                if erro_navegacao is not None and not _baixar_via_requisicao(
                    contexto, url, temp, referer=pagina_inicial
                ):
                    titulo = ""
                    try:
                        titulo = pagina.title()
                    except Exception:
                        pass
                    raise DataExtractionError(
                        f"O navegador não recebeu o CSV em {timeout_s}s"
                        + (f" (página: '{titulo}')" if titulo else "")
                        + ". Se apareceu o captcha da Radware, rode sem --headless e resolva-o na janela."
                    ) from erro_navegacao
        finally:
            try:
                contexto.close()
            except Exception:
                pass  # o navegador pode já ter sido encerrado

    if not parece_csv_caixa(temp):
        temp.unlink(missing_ok=True)
        raise DataExtractionError(
            "O arquivo baixado pelo navegador não é o CSV da Caixa (provável página de bloqueio)."
        )

    temp.replace(destino)
    logger.info(f"CSV baixado pelo navegador e salvo em '{destino}'")
    return destino


def _baixar_via_requisicao(contexto, url: str, destino_temp: Path, referer: Optional[str] = None) -> bool:
    """Baixa ``url`` usando os cookies do contexto do navegador. True se veio o CSV."""
    logger = get_logger("browser_download")
    try:
        headers = {"Referer": referer} if referer else None
        resp = contexto.request.get(url, headers=headers, timeout=120_000)
        content_type = (resp.headers.get("content-type") or "").lower()
        if not resp.ok or "text/html" in content_type:
            logger.info(f"Requisição pelo navegador não trouxe o CSV (HTTP {resp.status}, {content_type or '?'}).")
            return False
        destino_temp.write_bytes(resp.body())
    except Exception as exc:
        logger.info(f"Requisição pelo navegador falhou ({exc.__class__.__name__}: {exc}).")
        return False

    if parece_csv_caixa(destino_temp):
        return True
    destino_temp.unlink(missing_ok=True)
    return False


def encontrar_csv_em_downloads(
    pasta: Optional[Union[Path, str]] = None,
    max_idade_horas: Optional[float] = 24,
) -> Optional[Path]:
    """Retorna o ``Lista_imoveis_geral*.csv`` válido mais recente da pasta, ou None.

    Considera variações de nome que o navegador cria, como
    ``Lista_imoveis_geral (1).csv``. Ignora arquivos mais antigos que
    ``max_idade_horas`` (use None para não limitar).
    """
    logger = get_logger("browser_download")
    pasta = Path(pasta) if pasta else pasta_downloads_padrao()
    if not pasta.is_dir():
        logger.warning(f"Pasta de downloads não encontrada: {pasta}")
        return None

    candidatos = sorted(pasta.glob(PADRAO_ARQUIVO_CSV), key=lambda c: c.stat().st_mtime, reverse=True)
    limite = datetime.now() - timedelta(hours=max_idade_horas) if max_idade_horas is not None else None

    for candidato in candidatos:
        modificado = datetime.fromtimestamp(candidato.stat().st_mtime)
        if limite is not None and modificado < limite:
            logger.warning(
                f"CSV mais recente em '{pasta}' é de {modificado:%d/%m/%Y %H:%M}, "
                f"mais antigo que {max_idade_horas}h; ignorando."
            )
            return None
        if parece_csv_caixa(candidato):
            logger.info(f"Usando CSV encontrado em Downloads: {candidato} ({modificado:%d/%m/%Y %H:%M})")
            return candidato
    return None


def copiar_csv(origem: Union[Path, str], destino: Union[Path, str]) -> Path:
    """Copia o CSV para o destino padrão do projeto e retorna o caminho de destino."""
    destino = Path(destino)
    destino.parent.mkdir(parents=True, exist_ok=True)
    shutil.copy2(origem, destino)
    return destino
