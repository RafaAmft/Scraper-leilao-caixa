#!/usr/bin/env python3
"""
Configuração e gerenciamento de cidades para o Scraper Imóveis Caixa
"""

import json
import os
from datetime import datetime
from typing import Dict, List, Any, Optional
from config.logging_config import get_logger

logger = get_logger('cidades')

class CidadesConfig:
    """Gerenciador de configuração de cidades"""
    
    def __init__(self, config_file: str = 'configuracao_cidades.json'):
        self.config_file = config_file
        self.config = self._carregar_configuracao()
    
    def _carregar_configuracao(self) -> Dict[str, Any]:
        """Carrega configuração das cidades"""
        try:
            if os.path.exists(self.config_file):
                with open(self.config_file, 'r', encoding='utf-8') as f:
                    config = json.load(f)
                    logger.info(f"✅ Configuração de cidades carregada: {self._contar_total_cidades(config)} cidades")
                    return config
            else:
                logger.warning(f"⚠️ Arquivo de configuração não encontrado: {self.config_file}")
                return self._criar_configuracao_padrao()
                
        except Exception as e:
            logger.error(f"❌ Erro ao carregar configuração: {e}")
            return self._criar_configuracao_padrao()
    
    def _criar_configuracao_padrao(self) -> Dict[str, Any]:
        """Cria configuração padrão se não existir"""
        config_padrao = {
            "data_configuracao": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "observacao": "Configuração padrão criada automaticamente",
            "cidades": {
                "SC": {
                    "4205407": "Florianópolis",
                    "4208203": "Joinville",
                    "4216602": "São José"
                },
                "SP": {
                    "3550308": "São Paulo",
                    "3509502": "Campinas",
                    "3548708": "Ribeirão Preto"
                },
                "RS": {
                    "4314902": "Porto Alegre",
                    "4304606": "Canoas",
                    "4311205": "Novo Hamburgo"
                }
            }
        }
        
        logger.info("🆕 Criando configuração padrão de cidades")
        self._salvar_configuracao(config_padrao)
        return config_padrao
    
    def _contar_total_cidades(self, config: Dict[str, Any]) -> int:
        """Conta total de cidades na configuração"""
        total = 0
        for estado, cidades in config.get('cidades', {}).items():
            total += len(cidades)
        return total
    
    def _salvar_configuracao(self, config: Dict[str, Any]) -> bool:
        """Salva configuração em arquivo"""
        try:
            # Fazer backup se arquivo existir
            if os.path.exists(self.config_file):
                backup_file = f"{self.config_file}.backup_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
                os.rename(self.config_file, backup_file)
                logger.info(f"💾 Backup criado: {backup_file}")
            
            # Salvar nova configuração
            with open(self.config_file, 'w', encoding='utf-8') as f:
                json.dump(config, f, indent=2, ensure_ascii=False)
            
            logger.info(f"✅ Configuração salva em: {self.config_file}")
            return True
            
        except Exception as e:
            logger.error(f"❌ Erro ao salvar configuração: {e}")
            return False
    
    def obter_cidades_por_estado(self, estado: str) -> Dict[str, str]:
        """Retorna cidades de um estado específico"""
        return self.config.get('cidades', {}).get(estado, {})
    
    def obter_todos_estados(self) -> List[str]:
        """Retorna lista de todos os estados configurados"""
        return list(self.config.get('cidades', {}).keys())
    
    def obter_todas_cidades(self) -> List[Dict[str, str]]:
        """Retorna lista de todas as cidades com informações completas"""
        cidades = []
        for estado, cidades_estado in self.config.get('cidades', {}).items():
            for codigo, nome in cidades_estado.items():
                cidades.append({
                    'estado': estado,
                    'codigo': codigo,
                    'nome': nome
                })
        return cidades
    
    def adicionar_cidade(self, estado: str, codigo: str, nome: str) -> bool:
        """Adiciona uma nova cidade à configuração"""
        try:
            if estado not in self.config['cidades']:
                self.config['cidades'][estado] = {}
            
            self.config['cidades'][estado][codigo] = nome
            self.config['data_configuracao'] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            
            logger.info(f"✅ Cidade adicionada: {nome} ({estado}) - Código: {codigo}")
            return self._salvar_configuracao(self.config)
            
        except Exception as e:
            logger.error(f"❌ Erro ao adicionar cidade: {e}")
            return False
    
    def remover_cidade(self, estado: str, codigo: str) -> bool:
        """Remove uma cidade da configuração"""
        try:
            if estado in self.config['cidades'] and codigo in self.config['cidades'][estado]:
                nome = self.config['cidades'][estado][codigo]
                del self.config['cidades'][estado][codigo]
                
                # Remover estado se não tiver mais cidades
                if not self.config['cidades'][estado]:
                    del self.config['cidades'][estado]
                
                self.config['data_configuracao'] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                
                logger.info(f"✅ Cidade removida: {nome} ({estado}) - Código: {codigo}")
                return self._salvar_configuracao(self.config)
            else:
                logger.warning(f"⚠️ Cidade não encontrada: {estado} - {codigo}")
                return False
                
        except Exception as e:
            logger.error(f"❌ Erro ao remover cidade: {e}")
            return False
    
    def validar_configuracao(self) -> Dict[str, Any]:
        """Valida a configuração atual"""
        resultados = {
            'valida': True,
            'erros': [],
            'avisos': [],
            'estatisticas': {}
        }
        
        try:
            # Verificar estrutura básica
            if 'cidades' not in self.config:
                resultados['valida'] = False
                resultados['erros'].append("Campo 'cidades' não encontrado")
                return resultados
            
            # Estatísticas
            total_estados = len(self.config['cidades'])
            total_cidades = self._contar_total_cidades(self.config)
            resultados['estatisticas'] = {
                'total_estados': total_estados,
                'total_cidades': total_cidades
            }
            
            # Validar cada estado e cidade
            for estado, cidades in self.config['cidades'].items():
                if not cidades:
                    resultados['avisos'].append(f"Estado {estado} não tem cidades configuradas")
                    continue
                
                for codigo, nome in cidades.items():
                    # Validar código da cidade
                    if not codigo.isdigit():
                        resultados['erros'].append(f"Código inválido para {nome} ({estado}): {codigo}")
                        resultados['valida'] = False
                    
                    # Validar nome da cidade
                    if not nome or len(nome.strip()) < 2:
                        resultados['erros'].append(f"Nome inválido para cidade em {estado}: {nome}")
                        resultados['valida'] = False
            
            # Verificar se há cidades configuradas
            if total_cidades == 0:
                resultados['avisos'].append("Nenhuma cidade configurada")
            
            # Verificar data de configuração
            if 'data_configuracao' not in self.config:
                resultados['avisos'].append("Data de configuração não encontrada")
            
        except Exception as e:
            resultados['valida'] = False
            resultados['erros'].append(f"Erro durante validação: {e}")
        
        return resultados
    
    def gerar_relatorio_configuracao(self) -> str:
        """Gera relatório da configuração atual"""
        validacao = self.validar_configuracao()
        
        relatorio = f"""
📋 RELATÓRIO DE CONFIGURAÇÃO DE CIDADES
Data: {datetime.now().strftime('%d/%m/%Y %H:%M:%S')}
Arquivo: {self.config_file}

📊 ESTATÍSTICAS:
- Total de estados: {validacao['estatisticas'].get('total_estados', 0)}
- Total de cidades: {validacao['estatisticas'].get('total_cidades', 0)}

🏙️ CIDADES POR ESTADO:
"""
        
        for estado, cidades in self.config.get('cidades', {}).items():
            relatorio += f"\n{estado}:"
            for codigo, nome in cidades.items():
                relatorio += f"\n  - {codigo}: {nome}"
        
        relatorio += f"\n\n✅ VALIDAÇÃO: {'VÁLIDA' if validacao['valida'] else 'INVÁLIDA'}"
        
        if validacao['erros']:
            relatorio += "\n\n❌ ERROS:"
            for erro in validacao['erros']:
                relatorio += f"\n  - {erro}"
        
        if validacao['avisos']:
            relatorio += "\n\n⚠️ AVISOS:"
            for aviso in validacao['avisos']:
                relatorio += f"\n  - {aviso}"
        
        return relatorio
    
    def fazer_backup(self) -> str:
        """Faz backup da configuração atual"""
        try:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            backup_file = f"configuracao_cidades_backup_{timestamp}.json"
            
            with open(backup_file, 'w', encoding='utf-8') as f:
                json.dump(self.config, f, indent=2, ensure_ascii=False)
            
            logger.info(f"💾 Backup criado: {backup_file}")
            return backup_file
            
        except Exception as e:
            logger.error(f"❌ Erro ao criar backup: {e}")
            return ""

# Função de conveniência
def carregar_configuracao_cidades(config_file: str = 'configuracao_cidades.json') -> CidadesConfig:
    """Função de conveniência para carregar configuração"""
    return CidadesConfig(config_file)

