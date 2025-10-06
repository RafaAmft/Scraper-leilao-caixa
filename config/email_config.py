#!/usr/bin/env python3
"""
Configuração e envio de emails para o Scraper Imóveis Caixa
"""

import smtplib
import socket
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email import encoders
from datetime import datetime
import time
import json
import os
from typing import List, Dict, Any, Optional
from config.logging_config import get_logger
from utils.retry import retry_on_failure

logger = get_logger('email')

class EmailConfig:
    """Configuração de email"""
    
    def __init__(self):
        self.smtp_server = 'smtp.gmail.com'
        self.smtp_port = 587
        self.timeout = 60
        self.senha_app = "hfvk igne yago hwou"  # Senha de app fornecida
        
    def carregar_config_gmail(self) -> Dict[str, Any]:
        """Carrega configuração do Gmail com múltiplos destinatários"""
        script_dir = os.path.dirname(os.path.abspath(__file__))
        config_dir = os.path.dirname(script_dir)
        config_file = os.path.join(config_dir, "gmail_config_multiplos.json")
        
        if os.path.exists(config_file):
            try:
                with open(config_file, 'r', encoding='utf-8') as f:
                    config = json.load(f)
                    logger.info(f"✅ Configuração de email carregada: {len(config.get('email_destinatarios', []))} destinatários")
                    return config
            except Exception as e:
                logger.error(f"❌ Erro ao carregar configuração de email: {e}")
        
        logger.warning("⚠️ Configuração de email não encontrada, usando padrão")
        return {
            'email_remetente': None,
            'email_destinatarios': []
        }

class EmailSender:
    """Enviador de emails com retry automático"""
    
    def __init__(self):
        self.config = EmailConfig()
        self.gmail_config = self.config.carregar_config_gmail()
    
    @retry_on_failure(max_attempts=3, delay=5)
    def enviar_email_simples(self, destinatario: str, assunto: str, corpo: str) -> bool:
        """Envia email simples com retry automático"""
        try:
            email_remetente = self.gmail_config.get('email_remetente')
            if not email_remetente:
                logger.error("❌ Email remetente não configurado")
                return False
            
            # Criar mensagem
            msg = MIMEMultipart()
            msg['From'] = email_remetente
            msg['To'] = destinatario
            msg['Subject'] = assunto
            msg.attach(MIMEText(corpo, 'plain', 'utf-8'))
            
            # Enviar email
            return self._enviar_mensagem(msg, destinatario)
            
        except Exception as e:
            logger.error(f"❌ Erro ao criar email: {e}")
            raise
    
    @retry_on_failure(max_attempts=3, delay=5)
    def enviar_email_com_anexo(self, destinatario: str, assunto: str, corpo: str, 
                               anexo_conteudo: str, nome_anexo: str) -> bool:
        """Envia email com anexo com retry automático"""
        try:
            email_remetente = self.gmail_config.get('email_remetente')
            if not email_remetente:
                logger.error("❌ Email remetente não configurado")
                return False
            
            # Criar mensagem
            msg = MIMEMultipart()
            msg['From'] = email_remetente
            msg['To'] = destinatario
            msg['Subject'] = assunto
            
            # Corpo do email
            msg.attach(MIMEText(corpo, 'plain', 'utf-8'))
            
            # Anexo
            anexo = MIMEText(anexo_conteudo, 'plain', 'utf-8')
            anexo.add_header('Content-Disposition', 'attachment', filename=nome_anexo)
            msg.attach(anexo)
            
            # Enviar email
            return self._enviar_mensagem(msg, destinatario)
            
        except Exception as e:
            logger.error(f"❌ Erro ao criar email com anexo: {e}")
            raise
    
    def _enviar_mensagem(self, msg: MIMEMultipart, destinatario: str) -> bool:
        """Envia mensagem via SMTP"""
        try:
            logger.info(f"📧 Conectando ao servidor SMTP...")
            server = smtplib.SMTP(self.config.smtp_server, self.config.smtp_port, 
                                timeout=self.config.timeout)
            server.starttls()
            
            logger.info(f"🔐 Fazendo login...")
            server.login(self.gmail_config['email_remetente'], self.config.senha_app)
            
            logger.info(f"📤 Enviando email para {destinatario}...")
            server.send_message(msg)
            server.quit()
            
            logger.info(f"✅ Email enviado com sucesso para {destinatario}")
            return True
            
        except smtplib.SMTPAuthenticationError as e:
            logger.error(f"❌ Erro de autenticação: {e}")
            raise
        except smtplib.SMTPRecipientsRefused as e:
            logger.error(f"❌ Destinatário recusado: {e}")
            raise
        except (socket.timeout, socket.gaierror, ConnectionError) as e:
            logger.error(f"❌ Erro de conectividade: {e}")
            raise
        except Exception as e:
            logger.error(f"❌ Erro inesperado: {e}")
            raise
    
    def enviar_relatorio_multiplos(self, relatorio: str, relatorio_detalhado: str) -> Dict[str, Any]:
        """Envia relatório para múltiplos destinatários"""
        email_remetente = self.gmail_config.get('email_remetente')
        email_destinatarios = self.gmail_config.get('email_destinatarios', [])
        
        if not email_remetente:
            logger.error("❌ Email remetente não configurado!")
            return {'success': False, 'error': 'Email remetente não configurado'}
        
        if not email_destinatarios:
            logger.error("❌ Nenhum destinatário configurado!")
            return {'success': False, 'error': 'Nenhum destinatário configurado'}
        
        logger.info(f"📧 Enviando para {len(email_destinatarios)} destinatário(s)...")
        
        # Estatísticas de envio
        resultados = {
            'total_destinatarios': len(email_destinatarios),
            'emails_enviados': 0,
            'emails_falharam': 0,
            'destinatarios_sucesso': [],
            'destinatarios_falha': [],
            'success': True
        }
        
        # Enviar para cada destinatário
        for i, email_destinatario in enumerate(email_destinatarios, 1):
            logger.info(f"📧 [{i}/{len(email_destinatarios)}] Enviando para: {email_destinatario}")
            
            try:
                assunto = f"Relatório de Imóveis - {datetime.now().strftime('%d/%m/%Y')}"
                nome_anexo = f'relatorio_detalhado_{datetime.now().strftime("%Y%m%d_%H%M%S")}.txt'
                
                sucesso = self.enviar_email_com_anexo(
                    email_destinatario, assunto, relatorio, relatorio_detalhado, nome_anexo
                )
                
                if sucesso:
                    resultados['emails_enviados'] += 1
                    resultados['destinatarios_sucesso'].append(email_destinatario)
                else:
                    resultados['emails_falharam'] += 1
                    resultados['destinatarios_falha'].append(email_destinatario)
                    
            except Exception as e:
                logger.error(f"❌ Falha ao enviar para {email_destinatario}: {e}")
                resultados['emails_falharam'] += 1
                resultados['destinatarios_falha'].append(email_destinatario)
        
        # Resumo final
        if resultados['emails_falharam'] > 0:
            resultados['success'] = False
            logger.warning(f"⚠️ {resultados['emails_falharam']} emails falharam")
        
        logger.info(f"📊 Resumo: {resultados['emails_enviados']} enviados, {resultados['emails_falharam']} falharam")
        return resultados

# Função de conveniência para envio rápido
def enviar_email_relatorio(relatorio: str, relatorio_detalhado: str) -> Dict[str, Any]:
    """Função de conveniência para envio de relatório"""
    sender = EmailSender()
    return sender.enviar_relatorio_multiplos(relatorio, relatorio_detalhado)

