#!/usr/bin/env python3
"""
Sistema de validação de dados para o Scraper Imóveis Caixa
"""

import re
import json
from typing import Dict, Any, List, Tuple, Optional
from datetime import datetime
from config.logging_config import get_logger

logger = get_logger('validation')

class DataValidator:
    """Validador de dados de imóveis"""
    
    def __init__(self):
        # Campos obrigatórios para um imóvel válido
        self.required_fields = ['id_imovel', 'cidade', 'nome_imovel', 'valor']
        
        # Padrões de validação
        self.patterns = {
            'valor': r'R\$\s*\d{1,3}(?:\.\d{3})*(?:,\d{2})?$',
            'id_imovel': r'^\d+$',
            'cidade': r'^[A-Z\s]+$',
            'nome_imovel': r'^.+$'
        }
        
        # Métricas de validação
        self.metrics = {
            'total_validated': 0,
            'valid_count': 0,
            'invalid_count': 0,
            'missing_fields': {},
            'format_errors': {},
            'duplicates_found': 0
        }
    
    def validate_imovel(self, imovel: Dict[str, Any]) -> Tuple[bool, List[str]]:
        """
        Valida um imóvel individual
        
        Args:
            imovel: Dicionário com dados do imóvel
            
        Returns:
            Tuple (é_válido, lista_de_erros)
        """
        errors = []
        
        # Verificar campos obrigatórios
        for field in self.required_fields:
            if not imovel.get(field):
                errors.append(f"Campo obrigatório '{field}' não encontrado")
                self.metrics['missing_fields'][field] = self.metrics['missing_fields'].get(field, 0) + 1
        
        # Validar formato dos campos
        if imovel.get('valor'):
            if not re.match(self.patterns['valor'], str(imovel['valor'])):
                errors.append(f"Formato de valor inválido: {imovel['valor']}")
                self.metrics['format_errors']['valor'] = self.metrics['format_errors'].get('valor', 0) + 1
        
        if imovel.get('id_imovel'):
            if not re.match(self.patterns['id_imovel'], str(imovel['id_imovel'])):
                errors.append(f"ID do imóvel deve ser numérico: {imovel['id_imovel']}")
                self.metrics['format_errors']['id_imovel'] = self.metrics['format_errors'].get('id_imovel', 0) + 1
        
        if imovel.get('cidade'):
            if not re.match(self.patterns['cidade'], str(imovel['cidade'])):
                errors.append(f"Formato de cidade inválido: {imovel['cidade']}")
                self.metrics['format_errors']['cidade'] = self.metrics['format_errors'].get('cidade', 0) + 1
        
        # Validações específicas
        if imovel.get('valor'):
            try:
                # Tentar converter valor para float
                valor_str = str(imovel['valor']).replace('R$', '').replace('.', '').replace(',', '.').strip()
                valor_float = float(valor_str)
                if valor_float <= 0:
                    errors.append(f"Valor deve ser maior que zero: {imovel['valor']}")
            except ValueError:
                errors.append(f"Valor não pode ser convertido para número: {imovel['valor']}")
        
        # Atualizar métricas
        self.metrics['total_validated'] += 1
        if not errors:
            self.metrics['valid_count'] += 1
        else:
            self.metrics['invalid_count'] += 1
        
        return len(errors) == 0, errors
    
    def validate_imoveis_batch(self, imoveis: List[Dict[str, Any]]) -> Dict[str, Any]:
        """
        Valida um lote de imóveis
        
        Args:
            imoveis: Lista de imóveis para validar
            
        Returns:
            Dicionário com resultados da validação
        """
        logger.info(f"🔍 Validando lote de {len(imoveis)} imóveis...")
        
        validation_results = {
            'valid_imoveis': [],
            'invalid_imoveis': [],
            'validation_summary': {},
            'quality_score': 0.0
        }
        
        # Validar cada imóvel
        for imovel in imoveis:
            is_valid, errors = self.validate_imovel(imovel)
            
            if is_valid:
                validation_results['valid_imoveis'].append(imovel)
            else:
                imovel['validation_errors'] = errors
                validation_results['invalid_imoveis'].append(imovel)
        
        # Remover duplicatas
        unique_imoveis = self.remove_duplicates(validation_results['valid_imoveis'])
        duplicates_removed = len(validation_results['valid_imoveis']) - len(unique_imoveis)
        validation_results['valid_imoveis'] = unique_imoveis
        self.metrics['duplicates_found'] += duplicates_removed
        
        # Calcular score de qualidade
        total_imoveis = len(imoveis)
        if total_imoveis > 0:
            quality_score = (len(validation_results['valid_imoveis']) / total_imoveis) * 100
            validation_results['quality_score'] = round(quality_score, 2)
        
        # Resumo da validação
        validation_results['validation_summary'] = {
            'total_imoveis': total_imoveis,
            'valid_imoveis': len(validation_results['valid_imoveis']),
            'invalid_imoveis': len(validation_results['invalid_imoveis']),
            'duplicates_removed': duplicates_removed,
            'quality_score': validation_results['quality_score'],
            'validation_metrics': self.metrics.copy()
        }
        
        logger.info(f"✅ Validação concluída: {validation_results['validation_summary']}")
        
        return validation_results
    
    def remove_duplicates(self, imoveis: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """
        Remove imóveis duplicados baseado no ID
        
        Args:
            imoveis: Lista de imóveis
            
        Returns:
            Lista de imóveis sem duplicatas
        """
        seen_ids = set()
        unique_imoveis = []
        
        for imovel in imoveis:
            imovel_id = imovel.get('id_imovel', '')
            if imovel_id and imovel_id not in seen_ids:
                seen_ids.add(imovel_id)
                unique_imoveis.append(imovel)
        
        return unique_imoveis
    
    def generate_validation_report(self, validation_results: Dict[str, Any]) -> str:
        """
        Gera relatório de validação
        
        Args:
            validation_results: Resultados da validação
            
        Returns:
            Relatório formatado em texto
        """
        summary = validation_results['validation_summary']
        
        report = f"""
📊 RELATÓRIO DE VALIDAÇÃO DE DADOS
{'='*50}

📈 RESUMO GERAL:
   • Total de imóveis: {summary['total_imoveis']}
   • Imóveis válidos: {summary['valid_imoveis']}
   • Imóveis inválidos: {summary['invalid_imoveis']}
   • Duplicatas removidas: {summary['duplicates_removed']}
   • Score de qualidade: {summary['quality_score']}%

🔍 DETALHES DA VALIDAÇÃO:
   • Total validado: {self.metrics['total_validated']}
   • Válidos: {self.metrics['valid_count']}
   • Inválidos: {self.metrics['invalid_count']}

❌ CAMPOS FALTANDO:
"""
        
        for field, count in self.metrics['missing_fields'].items():
            report += f"   • {field}: {count} vezes\n"
        
        if not self.metrics['missing_fields']:
            report += "   • Nenhum campo obrigatório faltando\n"
        
        report += "\n⚠️ ERROS DE FORMATO:\n"
        
        for field, count in self.metrics['format_errors'].items():
            report += f"   • {field}: {count} vezes\n"
        
        if not self.metrics['format_errors']:
            report += "   • Nenhum erro de formato encontrado\n"
        
        # Detalhes dos imóveis inválidos
        if validation_results['invalid_imoveis']:
            report += f"\n❌ IMÓVEIS INVÁLIDOS (primeiros 5):\n"
            for i, imovel in enumerate(validation_results['invalid_imoveis'][:5], 1):
                report += f"   {i}. {imovel.get('nome_imovel', 'N/A')} - {imovel.get('cidade', 'N/A')}\n"
                for error in imovel.get('validation_errors', [])[:2]:  # Primeiros 2 erros
                    report += f"      • {error}\n"
        
        report += f"\n📅 Data/Hora: {datetime.now().strftime('%d/%m/%Y %H:%M:%S')}"
        report += f"\n{'='*50}"
        
        return report
    
    def save_validation_report(self, validation_results: Dict[str, Any], filename: str = None) -> str:
        """
        Salva relatório de validação em arquivo
        
        Args:
            validation_results: Resultados da validação
            filename: Nome do arquivo (opcional)
            
        Returns:
            Caminho do arquivo salvo
        """
        if filename is None:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"relatorio_validacao_{timestamp}.txt"
        
        report = self.generate_validation_report(validation_results)
        
        with open(filename, 'w', encoding='utf-8') as f:
            f.write(report)
        
        logger.info(f"📄 Relatório de validação salvo em: {filename}")
        return filename
    
    def get_validation_metrics(self) -> Dict[str, Any]:
        """
        Retorna métricas de validação
        
        Returns:
            Dicionário com métricas
        """
        return self.metrics.copy()
    
    def reset_metrics(self):
        """Reseta métricas de validação"""
        self.metrics = {
            'total_validated': 0,
            'valid_count': 0,
            'invalid_count': 0,
            'missing_fields': {},
            'format_errors': {},
            'duplicates_found': 0
        }
        logger.info("🔄 Métricas de validação resetadas")

# Funções utilitárias
def validate_single_imovel(imovel: Dict[str, Any]) -> Tuple[bool, List[str]]:
    """
    Valida um imóvel individual (função de conveniência)
    
    Args:
        imovel: Dicionário com dados do imóvel
        
    Returns:
        Tuple (é_válido, lista_de_erros)
    """
    validator = DataValidator()
    return validator.validate_imovel(imovel)

def validate_imoveis_file(filepath: str) -> Dict[str, Any]:
    """
    Valida imóveis de um arquivo JSON ou CSV
    
    Args:
        filepath: Caminho para o arquivo
        
    Returns:
        Resultados da validação
    """
    import pandas as pd
    
    validator = DataValidator()
    
    try:
        if filepath.endswith('.json'):
            with open(filepath, 'r', encoding='utf-8') as f:
                imoveis = json.load(f)
        elif filepath.endswith('.csv'):
            df = pd.read_csv(filepath, encoding='utf-8')
            imoveis = df.to_dict('records')
        else:
            raise ValueError("Formato de arquivo não suportado. Use .json ou .csv")
        
        return validator.validate_imoveis_batch(imoveis)
        
    except Exception as e:
        logger.error(f"❌ Erro ao ler arquivo {filepath}: {e}")
        return {
            'valid_imoveis': [],
            'invalid_imoveis': [],
            'validation_summary': {
                'error': str(e)
            },
            'quality_score': 0.0
        }

# Teste do sistema
if __name__ == "__main__":
    from config.logging_config import setup_logging
    
    # Configurar logging
    setup_logging(log_level=logging.INFO)
    
    # Teste de validação
    validator = DataValidator()
    
    # Imóveis de teste
    imoveis_teste = [
        {
            'id_imovel': '12345',
            'cidade': 'JOINVILLE',
            'nome_imovel': 'Casa Teste',
            'valor': 'R$ 150.000,00'
        },
        {
            'id_imovel': '67890',
            'cidade': 'FLORIANOPOLIS',
            'nome_imovel': 'Apartamento Teste',
            'valor': 'R$ 200.000,00'
        },
        {
            'id_imovel': '11111',
            'cidade': 'BLUMENAU',
            'nome_imovel': '',  # Inválido
            'valor': 'R$ 100.000,00'
        }
    ]
    
    # Validar lote
    resultados = validator.validate_imoveis_batch(imoveis_teste)
    
    # Gerar relatório
    relatorio = validator.generate_validation_report(resultados)
    print(relatorio)
    
    # Salvar relatório
    arquivo_relatorio = validator.save_validation_report(resultados)
    print(f"\n📄 Relatório salvo em: {arquivo_relatorio}")
    
    print("✅ Sistema de validação testado com sucesso!")

