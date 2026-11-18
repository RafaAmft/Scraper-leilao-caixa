#!/usr/bin/env python3
"""
Script automático para buscar imóveis em todas as cidades configuradas
a partir da lista oficial CSV da Caixa (download-lista.asp),
com geração de relatórios e envio por e-mail para múltiplos destinatários.
"""

import argparse
from datetime import datetime
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import json
import os
import smtplib
import socket
import sys
import time
from typing import Optional

# Adicionar o diretório src ao path
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "src"))

from config.logging_config import get_logger, setup_logging
from scraper_caixa.csv_loader import carregar_ou_baixar_csv, filtrar_cidades_configuradas
from scraper_caixa.gmail_oauth import (
    DEFAULT_CREDENTIALS_PATH,
    DEFAULT_TOKEN_PATH,
    enviar_email_oauth,
    obter_servico_gmail,
)


def carregar_configuracao(caminho: str = "configuracao_cidades.json"):
    """Carrega configuração das cidades."""
    try:
        with open(caminho, "r", encoding="utf-8") as f:
            return json.load(f)
    except FileNotFoundError:
        print(f"❌ Arquivo de configuração '{caminho}' não encontrado!")
        return None


def carregar_config_gmail():
    """Carrega a configuração do Gmail com múltiplos destinatários."""
    script_dir = os.path.dirname(os.path.abspath(__file__))
    config_dir = (
        os.path.join(script_dir, "config")
        if not script_dir.endswith("config")
        else script_dir
    )
    config_file = os.path.join(config_dir, "gmail_config_multiplos.json")

    if os.path.exists(config_file):
        try:
            with open(config_file, "r", encoding="utf-8") as f:
                return json.load(f)
        except Exception as e:
            print(f"❌ Erro ao carregar configuração de e-mail: {e}")

    return {"email_remetente": None, "email_destinatarios": []}


def _obter_senha_app(config_gmail: dict) -> Optional[str]:
    """Obtém a senha de app do Gmail via variável de ambiente ou configuração local."""
    return os.getenv("GMAIL_APP_PASSWORD") or config_gmail.get("senha_app")


def _criar_mensagem_email(
    remetente: str,
    destinatario: str,
    relatorio: str,
    relatorio_detalhado: str,
    timestamp_anexo: str,
) -> MIMEMultipart:
    msg = MIMEMultipart()
    msg["From"] = remetente
    msg["To"] = destinatario
    msg["Subject"] = f"Relatório de Imóveis - {datetime.now().strftime('%d/%m/%Y')}"

    corpo = f"""
{relatorio}

---
Relatório detalhado anexado.
Gerado automaticamente pelo Scraper Imóveis Caixa
"""
    msg.attach(MIMEText(corpo, "plain", "utf-8"))

    relatorio_anexo = MIMEText(relatorio_detalhado, "plain", "utf-8")
    relatorio_anexo.add_header(
        "Content-Disposition",
        "attachment",
        filename=f"relatorio_detalhado_{timestamp_anexo}.txt",
    )
    msg.attach(relatorio_anexo)
    return msg


def _enviar_via_oauth2(
    email_remetente: Optional[str],
    email_destinatarios: list,
    assunto: str,
    corpo: str,
    nome_anexo: str,
    relatorio_detalhado: str,
) -> int:
    """Envia e-mails usando a Gmail API via OAuth2 (sem senha de app)."""
    service = obter_servico_gmail(DEFAULT_CREDENTIALS_PATH, DEFAULT_TOKEN_PATH)
    emails_enviados = 0
    for i, destinatario in enumerate(email_destinatarios, 1):
        print(f"📧 [{i}/{len(email_destinatarios)}] Enviando via Gmail API para: {destinatario}")
        try:
            enviar_email_oauth(
                service=service,
                destinatario=destinatario,
                assunto=assunto,
                corpo=corpo,
                remetente=email_remetente,
                nome_anexo=nome_anexo,
                conteudo_anexo=relatorio_detalhado,
            )
            print(f"   ✅ Email enviado com sucesso para {destinatario}")
            emails_enviados += 1
        except Exception as e:
            print(f"   ❌ Erro ao enviar para {destinatario}: {e}")
    return emails_enviados


def enviar_email_relatorio(relatorio: str, relatorio_detalhado: str) -> int:
    """Envia relatório por email via Gmail API (OAuth2) ou fallback SMTP.

    Retorna a quantidade de e-mails enviados com sucesso.
    """
    config_gmail = carregar_config_gmail()
    email_remetente = config_gmail.get("email_remetente")
    email_destinatarios = config_gmail.get("email_destinatarios", [])

    if not email_destinatarios:
        print("❌ Nenhum destinatário configurado!")
        print("💡 Execute 'python config/configurar_gmail_multiplos.py' para configurar")
        return 0

    assunto = f"Relatório de Imóveis - {datetime.now().strftime('%d/%m/%Y')}"
    corpo = f"""
{relatorio}

---
Relatório detalhado anexado.
Gerado automaticamente pelo Scraper Imóveis Caixa
"""
    timestamp_anexo = datetime.now().strftime("%Y%m%d_%H%M%S")
    nome_anexo = f"relatorio_detalhado_{timestamp_anexo}.txt"

    usa_oauth2 = DEFAULT_CREDENTIALS_PATH.exists() or DEFAULT_TOKEN_PATH.exists()
    if usa_oauth2:
        print(f"🔐 Autenticando via Gmail API (OAuth2) para {len(email_destinatarios)} destinatário(s)...")
        try:
            emails_enviados = _enviar_via_oauth2(
                email_remetente,
                email_destinatarios,
                assunto,
                corpo,
                nome_anexo,
                relatorio_detalhado,
            )
        except Exception as e:
            print(f"❌ Erro na autenticação/envio via Gmail API: {e}")
            emails_enviados = 0
    else:
        senha_app = _obter_senha_app(config_gmail)
        if not email_remetente:
            print("❌ Email remetente não configurado!")
            print("💡 Execute 'python config/configurar_gmail_multiplos.py' para configurar")
            return 0
        if not senha_app:
            print("❌ Nenhuma credencial de e-mail configurada!")
            print(f"💡 Opção recomendada (sem senha): salve o OAuth2 em '{DEFAULT_CREDENTIALS_PATH}'")
            print("💡 Ou defina a variável de ambiente GMAIL_APP_PASSWORD para usar SMTP.")
            return 0

        print(f"📧 Enviando via SMTP para {len(email_destinatarios)} destinatário(s)...")
        max_tentativas = 3
        emails_enviados = 0

        for tentativa in range(max_tentativas):
            try:
                with smtplib.SMTP("smtp.gmail.com", 587, timeout=60) as server:
                    server.starttls()
                    server.login(email_remetente, senha_app)

                    for i, destinatario in enumerate(email_destinatarios, 1):
                        print(f"📧 [{i}/{len(email_destinatarios)}] Enviando para: {destinatario}")
                        try:
                            msg = _criar_mensagem_email(
                                email_remetente,
                                destinatario,
                                relatorio,
                                relatorio_detalhado,
                                timestamp_anexo,
                            )
                            server.send_message(msg)
                            print(f"   ✅ Email enviado com sucesso para {destinatario}")
                            emails_enviados += 1
                        except smtplib.SMTPRecipientsRefused as e:
                            print(f"   ❌ Destinatário recusado ({destinatario}): {e}")
                break
            except smtplib.SMTPAuthenticationError as e:
                print(f"   ❌ Erro de autenticação: {e}")
                break
            except (socket.timeout, socket.gaierror, ConnectionError) as e:
                print(f"   ❌ Erro de conectividade (tentativa {tentativa + 1}/{max_tentativas}): {e}")
                if tentativa < max_tentativas - 1:
                    time.sleep(10)
            except Exception as e:
                print(f"   ❌ Erro inesperado (tentativa {tentativa + 1}/{max_tentativas}): {e}")
                if tentativa < max_tentativas - 1:
                    time.sleep(5)

    if emails_enviados > 0:
        print(f"\n✅ {emails_enviados}/{len(email_destinatarios)} emails enviados com sucesso!")
    else:
        print("\n❌ Nenhum email foi enviado com sucesso")
        print("💡 O relatório foi salvo em arquivo local")

    return emails_enviados


def _formatar_imovel_relatorio(indice: int, imovel: dict) -> str:
    linhas = [f"\n  {indice}. {imovel['nome_imovel']}"]

    if imovel.get("quartos"):
        linhas.append(f"     🛏️ {imovel['quartos']} quarto(s)")

    valor_info = f"     💰 R$ {imovel['valor']}"
    if imovel.get("valor_avaliacao"):
        valor_info += f" (Avaliação: R$ {imovel['valor_avaliacao']}"
        if imovel.get("desconto"):
            valor_info += f" | Desconto: {imovel['desconto']}%"
        valor_info += ")"
    linhas.append(valor_info)

    if imovel.get("modalidade_venda"):
        modalidade_info = f"     🏷️ {imovel['modalidade_venda']}"
        if imovel.get("financiamento"):
            modalidade_info += f" | Financiamento: {imovel['financiamento']}"
        linhas.append(modalidade_info)

    if imovel.get("endereco"):
        linhas.append(f"     📍 {imovel['endereco']}")

    if imovel.get("link_direto"):
        linhas.append(f"     🔗 {imovel['link_direto']}")
    elif imovel.get("id_imovel"):
        linhas.append(
            f"     🔗 https://venda-imoveis.caixa.gov.br/sistema/detalhe-imovel.asp?hdnimovel={imovel['id_imovel']}"
        )

    return "\n".join(linhas)


def gerar_e_abrir_painel(df, destino, data_geracao, config, abrir, logger) -> None:
    """Gera o painel HTML; uma falha aqui não interrompe relatórios nem e-mail."""
    try:
        from scraper_caixa.painel import gerar_painel_html

        caminho = gerar_painel_html(df, destino, data_geracao=data_geracao, config_cidades=config)
        logger.info(f"📊 Painel com {len(df)} imóveis salvo em '{caminho}'")
        if abrir:
            import webbrowser

            webbrowser.open(caminho.resolve().as_uri())
    except Exception as e:
        logger.error(f"⚠️ Não foi possível gerar o painel: {e}")


def buscar_todas_cidades(
    caminho_csv: Optional[str] = None,
    enviar_email: bool = True,
    metodo_download: str = "auto",
    opcoes_download: Optional[dict] = None,
    painel: Optional[str] = "painel_imoveis.html",
    abrir_painel: bool = False,
):
    """Baixa/lê o CSV oficial da Caixa e gera relatórios para todas as cidades configuradas.

    Retorna o relatório resumido, ou None em caso de falha (configuração, download ou
    e-mail não enviado quando o envio foi solicitado).
    """
    setup_logging()
    logger = get_logger("scraper_automatico")

    config = carregar_configuracao()
    if not config:
        logger.error("❌ Falha ao carregar configuração!")
        return None

    logger.info("🚀 Iniciando busca de imóveis via CSV oficial da Caixa...")
    logger.info(f"📅 Data: {datetime.now().strftime('%d/%m/%Y %H:%M')}")

    try:
        df, data_geracao = carregar_ou_baixar_csv(
            caminho_csv=caminho_csv,
            baixar_se_necessario=caminho_csv is None,
            metodo_download=metodo_download,
            **(opcoes_download or {}),
        )
        resultados = filtrar_cidades_configuradas(df, config)
    except Exception as e:
        logger.error(f"❌ Erro ao processar CSV da Caixa: {e}")
        return None

    if painel:
        gerar_e_abrir_painel(df, painel, data_geracao, config, abrir_painel, logger)

    if data_geracao:
        logger.info(f"🗓️ Data de geração da lista Caixa: {data_geracao}")

    relatorio_completo = []
    imoveis_por_estado = {}
    total_imoveis = 0
    cidades_processadas = 0

    for estado, cidades in config["cidades"].items():
        imoveis_por_estado[estado] = 0
        logger.info(f"\n📍 Processando estado: {estado}")

        for _, nome in cidades.items():
            cidades_processadas += 1
            imoveis = resultados.get(estado, {}).get(nome, [])

            if imoveis:
                relatorio_cidade = f"\n🏙️ {nome}/{estado}: {len(imoveis)} imóveis encontrados"
                logger.info(f"✅ {nome}/{estado}: {len(imoveis)} imóveis encontrados")

                for i, imovel in enumerate(imoveis, 1):
                    relatorio_cidade += "\n" + _formatar_imovel_relatorio(i, imovel)

                relatorio_completo.append(relatorio_cidade)
                total_imoveis += len(imoveis)
                imoveis_por_estado[estado] += len(imoveis)
            else:
                relatorio_completo.append(f"\n🏙️ {nome}/{estado}: Nenhum imóvel encontrado")
                logger.warning(f"⚠️ {nome}/{estado}: Nenhum imóvel encontrado")

    data_atual = datetime.now().strftime("%d/%m/%Y")
    relatorio_resumido = f"Olá, hoje é dia {data_atual}, foram localizados"

    estados_com_imoveis = [
        f"{quantidade} imóveis em {estado}"
        for estado, quantidade in imoveis_por_estado.items()
        if quantidade > 0
    ]

    if estados_com_imoveis:
        relatorio_resumido += " " + ", ".join(estados_com_imoveis) + "."
    else:
        relatorio_resumido += " nenhum imóvel nas cidades monitoradas."

    info_lista = f"Lista Caixa gerada em: {data_geracao}\n" if data_geracao else ""
    relatorio_detalhado = f"""
📊 RELATÓRIO DETALHADO DE IMÓVEIS - CAIXA
Data da execução: {datetime.now().strftime('%d/%m/%Y %H:%M')}
{info_lista}Cidades processadas: {cidades_processadas}
Total de imóveis encontrados: {total_imoveis}

{''.join(relatorio_completo)}

---
Relatório gerado automaticamente
"""

    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename_resumido = f"relatorio_resumido_{timestamp}.txt"
    with open(filename_resumido, "w", encoding="utf-8") as f:
        f.write(relatorio_resumido)

    filename_detalhado = f"relatorio_detalhado_{timestamp}.txt"
    with open(filename_detalhado, "w", encoding="utf-8") as f:
        f.write(relatorio_detalhado)

    logger.info(f"✅ Relatório resumido salvo em '{filename_resumido}'")
    logger.info(f"✅ Relatório detalhado salvo em '{filename_detalhado}'")
    logger.info(f"📊 Total de imóveis encontrados: {total_imoveis}")
    logger.info(f"📧 RELATÓRIO RESUMIDO:\n   {relatorio_resumido}")

    if enviar_email:
        logger.info("📧 Preparando envio por email...")
        if enviar_email_relatorio(relatorio_resumido, relatorio_detalhado) == 0:
            logger.error("❌ Relatórios gerados, mas nenhum e-mail foi enviado.")
            return None

    return relatorio_resumido


def main():
    parser = argparse.ArgumentParser(
        description="Busca imóveis da Caixa a partir do CSV oficial."
    )
    parser.add_argument(
        "--csv",
        help="Caminho para um arquivo Lista_imoveis_geral.csv local (pula o download).",
        default=None,
    )
    parser.add_argument(
        "--sem-email",
        action="store_true",
        help="Gera os relatórios locais sem enviar e-mail.",
    )
    parser.add_argument(
        "--metodo",
        choices=["auto", "requests", "navegador", "downloads"],
        default="auto",
        help=(
            "Como obter o CSV: 'requests' (HTTP direto), 'navegador' (Chrome real via Playwright), "
            "'downloads' (CSV mais recente da pasta Downloads) ou 'auto' (tenta os três nessa ordem)."
        ),
    )
    parser.add_argument(
        "--headless",
        action="store_true",
        help="Abre o navegador sem janela (só funciona depois que o perfil já passou pelo captcha).",
    )
    parser.add_argument(
        "--janela-escondida",
        action="store_true",
        help=(
            "Abre o Chrome com janela, mas fora da área visível da tela. Mais confiável que "
            "--headless contra a proteção da Caixa; ideal para o Agendador de Tarefas."
        ),
    )
    parser.add_argument(
        "--perfil-navegador",
        default=None,
        help="Pasta do perfil persistente do navegador (padrão: navegador_perfil).",
    )
    parser.add_argument(
        "--pasta-downloads",
        default=None,
        help="Pasta onde procurar o CSV baixado manualmente (padrão: Downloads do usuário).",
    )
    parser.add_argument(
        "--painel",
        default="painel_imoveis.html",
        help="Arquivo do painel HTML com todos os imóveis do Brasil (padrão: painel_imoveis.html).",
    )
    parser.add_argument(
        "--sem-painel",
        action="store_true",
        help="Não gera o painel HTML.",
    )
    parser.add_argument(
        "--abrir-painel",
        action="store_true",
        help="Abre o painel no navegador ao final.",
    )
    parser.add_argument(
        "--auth-gmail",
        action="store_true",
        help="Executa apenas a autenticação OAuth2 do Gmail para gerar config/gmail_token.json.",
    )
    args = parser.parse_args()
    if args.auth_gmail:
        obter_servico_gmail(DEFAULT_CREDENTIALS_PATH, DEFAULT_TOKEN_PATH)
        print(f"✅ Autenticação OAuth2 concluída! Token salvo em '{DEFAULT_TOKEN_PATH}'.")
        return
    opcoes_download = {
        "headless": args.headless,
        "janela_escondida": args.janela_escondida,
        "perfil_navegador": args.perfil_navegador,
        "pasta_downloads": args.pasta_downloads,
    }
    resultado = buscar_todas_cidades(
        caminho_csv=args.csv,
        enviar_email=not args.sem_email,
        metodo_download=args.metodo,
        opcoes_download=opcoes_download,
        painel=None if args.sem_painel else args.painel,
        abrir_painel=args.abrir_painel,
    )
    if resultado is None:
        sys.exit(1)


if __name__ == "__main__":
    main()
