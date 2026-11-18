"""Publicação do painel HTML no GitHub Pages (branch ``gh-pages``).

Cada publicação cria, numa pasta temporária, um commit novo e sem histórico
contendo apenas ``index.html`` (o painel) e ``.nojekyll``, e o envia com
``--force`` para o branch ``gh-pages`` do mesmo repositório remoto. Assim o
branch guarda só a versão mais recente e o repositório não cresce a cada dia.

O repositório de trabalho do usuário não é alterado; o push usa as mesmas
credenciais do git já configuradas no computador.
"""

import os
from pathlib import Path
import re
import shutil
import stat
import subprocess
import sys
import tempfile
from typing import List, Optional, Union

from .logger import get_logger

DEFAULT_BRANCH = "gh-pages"
# Identidade fixa do commit de publicação: não expõe o e-mail do usuário e evita o
# bloqueio de privacidade de e-mail do GitHub (GH007).
_IDENTIDADE_PUBLICACAO = ("Scraper Leilao Caixa", "scraper-leilao-caixa@users.noreply.github.com")
_GITHUB_RE = re.compile(r"github\.com[:/](?P<dono>[^/]+)/(?P<repo>[^/]+?)(?:\.git)?/?$", re.IGNORECASE)


class PublicacaoError(RuntimeError):
    """Falha ao publicar o painel."""


def url_github_pages(remote_url: str) -> Optional[str]:
    """Converte a URL do remoto do GitHub no endereço do GitHub Pages do repositório."""
    m = _GITHUB_RE.search((remote_url or "").strip())
    if not m:
        return None
    dono, repo = m.group("dono"), m.group("repo")
    if repo.lower() == f"{dono.lower()}.github.io":
        return f"https://{dono.lower()}.github.io/"
    return f"https://{dono.lower()}.github.io/{repo}/"


def _git(args: List[str], cwd: Union[Path, str], timeout: int = 120) -> str:
    env = dict(os.environ)
    env["GIT_TERMINAL_PROMPT"] = "0"  # na tarefa agendada não há quem digite senha: falha rápido
    try:
        resultado = subprocess.run(
            ["git", *args],
            cwd=str(cwd),
            env=env,
            capture_output=True,
            text=True,
            encoding="utf-8",
            errors="replace",
            timeout=timeout,
        )
    except FileNotFoundError as exc:
        raise PublicacaoError("Git não encontrado no PATH.") from exc
    except subprocess.TimeoutExpired as exc:
        raise PublicacaoError(f"git {args[0]} demorou mais de {timeout}s.") from exc
    if resultado.returncode != 0:
        raise PublicacaoError(_mensagem_erro(args[0], resultado.stderr or resultado.stdout))
    return resultado.stdout.strip()


# (trecho procurado na saída do git, dica para o usuário)
_DICAS_ERRO = (
    ("email privacy", "O GitHub bloqueou o push por privacidade de e-mail (GH007). "
                      "Veja Settings > Emails > 'Block command line pushes that expose my email'."),
    ("gh013", "Uma regra (ruleset) do repositório bloqueou o push. Veja Settings > Rules > Rulesets."),
    ("protected branch", "O branch está protegido. Veja Settings > Branches."),
    ("could not read username", "Sem credencial do GitHub para push. Faça um 'git push' manual uma vez "
                                "para salvar a credencial no Gerenciador de Credenciais do Windows."),
    ("authentication failed", "Credencial do GitHub inválida ou expirada. Faça um 'git push' manual para renová-la."),
    ("permission to", "Esta conta não tem permissão de push neste repositório."),
    ("403", "O GitHub recusou o acesso (403): verifique a credencial e a permissão de push."),
)


def _mensagem_erro(comando: str, saida: str) -> str:
    """Resume a saída de erro do git mantendo as linhas que explicam o motivo."""
    linhas = [linha.strip() for linha in (saida or "").strip().splitlines() if linha.strip()]
    relevantes = [
        linha for linha in linhas
        if linha.lower().startswith(("remote:", "!", "error:", "fatal:", "hint:"))
        and linha.lower().strip() not in ("remote:",)
    ] or linhas
    resumo = " | ".join(relevantes[-8:]) if relevantes else "erro desconhecido"
    texto = (saida or "").lower()
    dica = next((d for trecho, d in _DICAS_ERRO if trecho in texto), None)
    return f"git {comando} falhou: {resumo}" + (f"\n    Dica: {dica}" if dica else "")


def _remover_pasta(pasta: Path) -> None:
    """Remove a pasta temporária; no Windows os objetos do git são somente leitura."""

    def liberar(func, caminho, _info):
        try:
            os.chmod(caminho, stat.S_IWRITE)
            func(caminho)
        except OSError:
            pass

    if sys.version_info >= (3, 12):
        shutil.rmtree(pasta, onexc=liberar)
    else:
        shutil.rmtree(pasta, onerror=liberar)


def publicar_painel_github_pages(
    painel: Union[Path, str],
    repo_dir: Union[Path, str] = ".",
    remote: str = "origin",
    branch: str = DEFAULT_BRANCH,
) -> Optional[str]:
    """Publica ``painel`` como ``index.html`` no branch ``branch`` e retorna a URL do Pages.

    Retorna None quando o remoto não é do GitHub (o push é feito mesmo assim).
    Levanta ``PublicacaoError`` em caso de falha.
    """
    logger = get_logger("publicacao")
    painel = Path(painel)
    repo_dir = Path(repo_dir)
    if not painel.is_file():
        raise PublicacaoError(f"Painel não encontrado: {painel}")

    remote_url = _git(["remote", "get-url", remote], repo_dir)
    nome, email = _IDENTIDADE_PUBLICACAO

    pasta = Path(tempfile.mkdtemp(prefix="publicacao_painel_"))
    try:
        _git(["init", "-q"], pasta)
        _git(["checkout", "-q", "-b", branch], pasta)
        shutil.copyfile(painel, pasta / "index.html")
        (pasta / ".nojekyll").write_text("", encoding="utf-8")
        _git(["add", "index.html", ".nojekyll"], pasta)
        _git(
            ["-c", f"user.name={nome}", "-c", f"user.email={email}",
             "commit", "-q", "-m", "Atualiza painel de imóveis"],
            pasta,
        )
        logger.info(f"Enviando painel para o branch '{branch}' de {remote_url} ...")
        _git(["push", "--force", "-q", remote_url, f"HEAD:refs/heads/{branch}"], pasta, timeout=300)
    finally:
        _remover_pasta(pasta)

    url = url_github_pages(remote_url)
    logger.info(f"Painel publicado{f': {url}' if url else ''}")
    return url
