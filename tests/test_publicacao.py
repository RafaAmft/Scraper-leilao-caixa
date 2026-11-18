"""Testes da publicação do painel no GitHub Pages (com um repositório remoto local)."""

from pathlib import Path
import subprocess
import sys

import pytest

sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "src"))

from scraper_caixa.publicacao import PublicacaoError, publicar_painel_github_pages, url_github_pages


def _git(*args, cwd):
    return subprocess.run(["git", *args], cwd=cwd, check=True, capture_output=True, text=True).stdout.strip()


@pytest.mark.parametrize(
    "remote,esperado",
    [
        ("https://github.com/RafaAmft/Scraper-leilao-caixa", "https://rafaamft.github.io/Scraper-leilao-caixa/"),
        ("https://github.com/RafaAmft/Scraper-leilao-caixa.git", "https://rafaamft.github.io/Scraper-leilao-caixa/"),
        ("git@github.com:RafaAmft/Scraper-leilao-caixa.git", "https://rafaamft.github.io/Scraper-leilao-caixa/"),
        ("https://github.com/fulano/fulano.github.io.git", "https://fulano.github.io/"),
        ("https://gitlab.com/x/y.git", None),
    ],
)
def test_url_github_pages(remote, esperado):
    assert url_github_pages(remote) == esperado


@pytest.fixture
def repos(tmp_path: Path):
    remoto = tmp_path / "remoto.git"
    _git("init", "-q", "--bare", str(remoto), cwd=tmp_path)
    local = tmp_path / "local"
    local.mkdir()
    _git("init", "-q", cwd=local)
    _git("remote", "add", "origin", str(remoto), cwd=local)
    return local, remoto


def test_publicar_cria_gh_pages_com_um_unico_commit(repos, tmp_path: Path):
    local, remoto = repos
    painel = tmp_path / "painel_imoveis.html"

    painel.write_text("<html>versao 1</html>", encoding="utf-8")
    assert publicar_painel_github_pages(painel, repo_dir=local) is None  # remoto não é do GitHub

    painel.write_text("<html>versao 2</html>", encoding="utf-8")
    publicar_painel_github_pages(painel, repo_dir=local)

    assert _git("show", "gh-pages:index.html", cwd=remoto) == "<html>versao 2</html>"
    assert _git("ls-tree", "--name-only", "gh-pages", cwd=remoto).split() == [".nojekyll", "index.html"]
    assert _git("rev-list", "--count", "gh-pages", cwd=remoto) == "1"
    # o repositório de trabalho não foi alterado
    assert _git("status", "--porcelain", cwd=local) == ""
    assert "gh-pages" not in _git("branch", "--list", cwd=local)


def test_publicar_sem_painel_ou_sem_remoto_falha(repos, tmp_path: Path):
    local, _ = repos
    with pytest.raises(PublicacaoError, match="Painel não encontrado"):
        publicar_painel_github_pages(tmp_path / "nao_existe.html", repo_dir=local)

    sem_remoto = tmp_path / "sem_remoto"
    sem_remoto.mkdir()
    _git("init", "-q", cwd=sem_remoto)
    painel = tmp_path / "p.html"
    painel.write_text("x", encoding="utf-8")
    with pytest.raises(PublicacaoError, match="remote"):
        publicar_painel_github_pages(painel, repo_dir=sem_remoto)


def test_commit_de_publicacao_usa_identidade_noreply(repos, tmp_path: Path):
    local, remoto = repos
    _git("config", "user.email", "pessoa@exemplo.com", cwd=local)
    painel = tmp_path / "p.html"
    painel.write_text("<html></html>", encoding="utf-8")

    publicar_painel_github_pages(painel, repo_dir=local)

    autor = _git("log", "-1", "--format=%an <%ae>", "gh-pages", cwd=remoto)
    assert autor == "Scraper Leilao Caixa <scraper-leilao-caixa@users.noreply.github.com>"


def test_push_recusado_mostra_motivo_do_remoto_e_dica(repos, tmp_path: Path):
    local, remoto = repos
    hook = remoto / "hooks" / "pre-receive"
    hook.write_text(
        "#!/bin/sh\n"
        "echo 'GH007: Your push would publish a private email address.' >&2\n"
        "echo 'push declined due to email privacy restrictions' >&2\n"
        "exit 1\n",
        encoding="utf-8",
    )
    hook.chmod(0o755)
    painel = tmp_path / "p.html"
    painel.write_text("<html></html>", encoding="utf-8")

    with pytest.raises(PublicacaoError) as erro:
        publicar_painel_github_pages(painel, repo_dir=local)

    mensagem = str(erro.value)
    assert "GH007" in mensagem
    assert "failed to push some refs" in mensagem
    assert "Dica:" in mensagem and "privacidade de e-mail" in mensagem
