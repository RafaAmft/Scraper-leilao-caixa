"""Módulo para envio de e-mails via Gmail API usando OAuth2 (sem senha de app)."""

import base64
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from pathlib import Path
from typing import Optional, Union

SCOPES = ["https://www.googleapis.com/auth/gmail.send"]
DEFAULT_CREDENTIALS_PATH = Path("config") / "gmail_credentials.json"
DEFAULT_TOKEN_PATH = Path("config") / "gmail_token.json"


def _importar_google_libs():
    try:
        from google.auth.transport.requests import Request
        from google.oauth2.credentials import Credentials
        from google_auth_oauthlib.flow import InstalledAppFlow
        from googleapiclient.discovery import build
    except ImportError as exc:
        raise ImportError(
            "Dependências da Gmail API não instaladas. Execute: "
            "pip install google-api-python-client google-auth-oauthlib google-auth-httplib2"
        ) from exc
    return Request, Credentials, InstalledAppFlow, build


def obter_servico_gmail(
    credentials_path: Union[Path, str] = DEFAULT_CREDENTIALS_PATH,
    token_path: Union[Path, str] = DEFAULT_TOKEN_PATH,
):
    """Autentica via OAuth2 (abrindo o navegador apenas na 1ª vez) e retorna o serviço Gmail."""
    Request, Credentials, InstalledAppFlow, build = _importar_google_libs()

    cred_file = Path(credentials_path)
    token_file = Path(token_path)
    creds = None

    if token_file.exists():
        creds = Credentials.from_authorized_user_file(str(token_file), SCOPES)

    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            if not cred_file.exists():
                raise FileNotFoundError(
                    f"Arquivo de credenciais OAuth2 não encontrado em '{cred_file}'. "
                    "Baixe o JSON de credenciais OAuth (Desktop app) no Google Cloud Console "
                    "e salve nesse caminho."
                )
            flow = InstalledAppFlow.from_client_secrets_file(str(cred_file), SCOPES)
            creds = flow.run_local_server(port=0)

        token_file.parent.mkdir(parents=True, exist_ok=True)
        token_file.write_text(creds.to_json(), encoding="utf-8")

    return build("gmail", "v1", credentials=creds)


def criar_mensagem_mime(
    remetente: Optional[str],
    destinatario: str,
    assunto: str,
    corpo: str,
    nome_anexo: Optional[str] = None,
    conteudo_anexo: Optional[str] = None,
) -> MIMEMultipart:
    """Monta a mensagem MIME com corpo em texto e anexo opcional."""
    msg = MIMEMultipart()
    if remetente:
        msg["From"] = remetente
    msg["To"] = destinatario
    msg["Subject"] = assunto
    msg.attach(MIMEText(corpo, "plain", "utf-8"))

    if nome_anexo and conteudo_anexo is not None:
        anexo = MIMEText(conteudo_anexo, "plain", "utf-8")
        anexo.add_header("Content-Disposition", "attachment", filename=nome_anexo)
        msg.attach(anexo)

    return msg


def enviar_email_oauth(
    service,
    destinatario: str,
    assunto: str,
    corpo: str,
    remetente: Optional[str] = None,
    nome_anexo: Optional[str] = None,
    conteudo_anexo: Optional[str] = None,
):
    """Envia um e-mail usando um serviço Gmail API já autenticado."""
    msg = criar_mensagem_mime(
        remetente=remetente,
        destinatario=destinatario,
        assunto=assunto,
        corpo=corpo,
        nome_anexo=nome_anexo,
        conteudo_anexo=conteudo_anexo,
    )
    raw = base64.urlsafe_b64encode(msg.as_bytes()).decode("utf-8")
    return service.users().messages().send(userId="me", body={"raw": raw}).execute()
