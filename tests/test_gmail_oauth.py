"""Testes unitários para o módulo gmail_oauth."""

import base64
from pathlib import Path
import sys
from unittest.mock import MagicMock, patch

import pytest

sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "src"))

from scraper_caixa.gmail_oauth import (
    criar_mensagem_mime,
    enviar_email_oauth,
    obter_servico_gmail,
)


def test_criar_mensagem_mime_com_anexo():
    msg = criar_mensagem_mime(
        remetente="remetente@gmail.com",
        destinatario="destino@gmail.com",
        assunto="Teste Relatório",
        corpo="Resumo do dia",
        nome_anexo="relatorio.txt",
        conteudo_anexo="Conteúdo detalhado",
    )
    assert msg["From"] == "remetente@gmail.com"
    assert msg["To"] == "destino@gmail.com"
    assert msg["Subject"] == "Teste Relatório"
    partes = msg.get_payload()
    assert len(partes) == 2
    assert "relatorio.txt" in partes[1].get("Content-Disposition", "")


def test_enviar_email_oauth_chama_api():
    mock_service = MagicMock()
    mock_send = mock_service.users.return_value.messages.return_value.send
    mock_send.return_value.execute.return_value = {"id": "msg-123"}

    resp = enviar_email_oauth(
        service=mock_service,
        destinatario="destino@gmail.com",
        assunto="Assunto",
        corpo="Corpo",
        remetente="remetente@gmail.com",
        nome_anexo="anexo.txt",
        conteudo_anexo="dados",
    )

    assert resp == {"id": "msg-123"}
    mock_send.assert_called_once()
    kwargs = mock_send.call_args.kwargs
    assert kwargs["userId"] == "me"
    raw_bytes = base64.urlsafe_b64decode(kwargs["body"]["raw"])
    assert b"destino@gmail.com" in raw_bytes
    assert b"anexo.txt" in raw_bytes


def test_obter_servico_gmail_sem_credenciais_levanta_erro(tmp_path: Path):
    with pytest.raises(FileNotFoundError):
        obter_servico_gmail(
            credentials_path=tmp_path / "nao_existe.json",
            token_path=tmp_path / "token.json",
        )


def test_obter_servico_gmail_com_token_valido(tmp_path: Path):
    token_file = tmp_path / "gmail_token.json"
    token_file.write_text("{}", encoding="utf-8")

    mock_creds = MagicMock()
    mock_creds.valid = True
    mock_creds.to_json.return_value = '{"token": "ok"}'

    with patch("google.oauth2.credentials.Credentials.from_authorized_user_file", return_value=mock_creds), \
         patch("googleapiclient.discovery.build", return_value="gmail_service") as mock_build:
        service = obter_servico_gmail(
            credentials_path=tmp_path / "gmail_credentials.json",
            token_path=token_file,
        )

    assert service == "gmail_service"
    mock_build.assert_called_once_with("gmail", "v1", credentials=mock_creds)
