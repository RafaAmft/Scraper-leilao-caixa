# 📋 PLANO DE AÇÃO DETALHADO - SCRAPER IMÓVEIS CAIXA
*Janeiro 2025 - Próximas 4 Semanas*

## 🎯 **VISÃO GERAL**

Este plano detalha as ações específicas para as próximas 4 semanas, focando em estabilização, expansão e preparação para o próximo nível do projeto.

---

## 📅 **SEMANA 1: ESTABILIZAÇÃO CRÍTICA**

### **Dia 1-2: Auditoria e Diagnóstico**
- [ ] **Auditoria completa do código**
  - Revisar `scraper_automatico.py` para bugs
  - Verificar `src/scraper_caixa/scraper.py` para problemas
  - Analisar logs de erro existentes
  - Identificar pontos de falha

- [ ] **Teste de estabilidade**
  - Executar testes em diferentes cenários
  - Testar com diferentes estados
  - Verificar timeout e retry
  - Validar sistema de email

### **Dia 3-4: Correções Críticas**
- [ ] **Implementar sistema de logs**
  ```python
  # Adicionar ao scraper_automatico.py
  import logging
  logging.basicConfig(
      level=logging.INFO,
      format='%(asctime)s - %(levelname)s - %(message)s',
      handlers=[
          logging.FileHandler(f'logs/scraper_{datetime.now().strftime("%Y%m%d")}.log'),
          logging.StreamHandler()
      ]
  )
  ```

- [ ] **Corrigir retry automático**
  - Implementar retry para falhas de rede
  - Adicionar timeout configurável
  - Melhorar tratamento de erros

### **Dia 5-7: Validação e Testes**
- [ ] **Testes extensivos**
  - Testar com todos os estados atuais
  - Validar sistema de email
  - Verificar geração de relatórios
  - Testar em diferentes horários

---

## 📅 **SEMANA 2: MELHORIAS E EXPANSÃO**

### **Dia 8-10: Relatórios HTML**
- [ ] **Criar template HTML**
  ```html
  <!-- templates/relatorio.html -->
  <!DOCTYPE html>
  <html>
  <head>
      <title>Relatório de Imóveis - {{data}}</title>
      <style>
          /* CSS responsivo */
      </style>
  </head>
  <body>
      <h1>Relatório de Imóveis - {{data}}</h1>
      <!-- Conteúdo dinâmico -->
  </body>
  </html>
  ```

- [ ] **Implementar geração HTML**
  - Usar Jinja2 para templates
  - Adicionar gráficos com Chart.js
  - Incluir links diretos para imóveis
  - Melhorar apresentação visual

### **Dia 11-12: Validação de Dados**
- [ ] **Implementar validação**
  ```python
  def validar_dados_imovel(imovel):
      campos_obrigatorios = ['id', 'endereco', 'valor', 'cidade']
      for campo in campos_obrigatorios:
          if not imovel.get(campo):
              return False
      return True
  ```

- [ ] **Métricas de qualidade**
  - Contador de dados válidos
  - Detecção de duplicatas
  - Relatório de qualidade

### **Dia 13-14: Novos Estados**
- [ ] **Adicionar 3-5 novos estados**
  - Acre (AC)
  - Alagoas (AL)
  - Amapá (AP)
  - Amazonas (AM)
  - Distrito Federal (DF)

---

## 📅 **SEMANA 3: EXPANSÃO E FILTROS**

### **Dia 15-17: Mais Estados**
- [ ] **Adicionar 5-7 estados**
  - Espírito Santo (ES)
  - Maranhão (MA)
  - Pará (PA)
  - Paraíba (PB)
  - Piauí (PI)
  - Rio Grande do Norte (RN)
  - Rondônia (RO)

### **Dia 18-19: Filtros Avançados**
- [ ] **Implementar novos filtros**
  ```python
  # Novos filtros no scraper
  filtros_avancados = {
      'area_min': 50,  # m²
      'area_max': 200,  # m²
      'vagas_garagem': 1,
      'tipo_construcao': 'residencial',
      'status': 'disponivel'
  }
  ```

- [ ] **Interface de configuração**
  - Arquivo JSON para filtros
  - Validação de filtros
  - Documentação dos filtros

### **Dia 20-21: Monitoramento Básico**
- [ ] **Sistema de monitoramento**
  ```python
  # Métricas básicas
  metricas = {
      'total_buscas': 0,
      'sucessos': 0,
      'falhas': 0,
      'tempo_medio': 0,
      'imoveis_encontrados': 0
  }
  ```

---

## 📅 **SEMANA 4: PREPARAÇÃO PARA DASHBOARD**

### **Dia 22-24: Estrutura do Dashboard**
- [ ] **Criar estrutura básica**
  ```
  dashboard/
  ├── static/
  │   ├── css/
  │   ├── js/
  │   └── images/
  ├── templates/
  ├── app.py
  └── requirements.txt
  ```

- [ ] **API básica com FastAPI**
  ```python
  from fastapi import FastAPI
  from fastapi.staticfiles import StaticFiles
  
  app = FastAPI()
  app.mount("/static", StaticFiles(directory="static"), name="static")
  
  @app.get("/api/imoveis")
  async def get_imoveis():
      # Retornar dados dos imóveis
      pass
  ```

### **Dia 25-26: Frontend Básico**
- [ ] **Página principal**
  - Lista de imóveis
  - Filtros interativos
  - Gráficos básicos
  - Responsivo

### **Dia 27-28: Integração e Testes**
- [ ] **Integrar com scraper existente**
  - Conectar API com dados
  - Testar funcionalidades
  - Validar performance
  - Documentar uso

---

## 🛠️ **TAREFAS TÉCNICAS DETALHADAS**

### **1. Sistema de Logs (Dia 1-2)**
```python
# config/logging_config.py
import logging
import os
from datetime import datetime

def setup_logging():
    # Criar diretório de logs
    os.makedirs('logs', exist_ok=True)
    
    # Configurar logging
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        handlers=[
            logging.FileHandler(f'logs/scraper_{datetime.now().strftime("%Y%m%d")}.log'),
            logging.StreamHandler()
        ]
    )
    
    return logging.getLogger(__name__)
```

### **2. Retry Automático (Dia 3-4)**
```python
# utils/retry.py
import time
import logging
from functools import wraps

def retry_on_failure(max_attempts=3, delay=5):
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            for attempt in range(max_attempts):
                try:
                    return func(*args, **kwargs)
                except Exception as e:
                    logging.warning(f"Tentativa {attempt + 1} falhou: {e}")
                    if attempt < max_attempts - 1:
                        time.sleep(delay)
                    else:
                        raise
            return None
        return wrapper
    return decorator
```

### **3. Validação de Dados (Dia 11-12)**
```python
# utils/validation.py
import re
from typing import Dict, Any

class DataValidator:
    @staticmethod
    def validate_imovel(imovel: Dict[str, Any]) -> bool:
        required_fields = ['id', 'endereco', 'valor', 'cidade']
        
        # Verificar campos obrigatórios
        for field in required_fields:
            if not imovel.get(field):
                return False
        
        # Validar formato do valor
        valor = str(imovel.get('valor', ''))
        if not re.match(r'R\$\s*\d+[.,]\d+', valor):
            return False
        
        # Validar ID (deve ser numérico)
        if not str(imovel.get('id', '')).isdigit():
            return False
        
        return True
    
    @staticmethod
    def remove_duplicates(imoveis: list) -> list:
        seen_ids = set()
        unique_imoveis = []
        
        for imovel in imoveis:
            if imovel.get('id') not in seen_ids:
                seen_ids.add(imovel.get('id'))
                unique_imoveis.append(imovel)
        
        return unique_imoveis
```

### **4. API FastAPI (Dia 22-24)**
```python
# dashboard/app.py
from fastapi import FastAPI, HTTPException
from fastapi.staticfiles import StaticFiles
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
import json
import os

app = FastAPI(title="Scraper Imóveis Caixa Dashboard")

# Configurar arquivos estáticos e templates
app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")

@app.get("/", response_class=HTMLResponse)
async def dashboard(request):
    return templates.TemplateResponse("dashboard.html", {"request": request})

@app.get("/api/imoveis")
async def get_imoveis():
    # Carregar dados dos imóveis
    try:
        with open('dados_imoveis/latest/imoveis.json', 'r') as f:
            imoveis = json.load(f)
        return {"imoveis": imoveis, "total": len(imoveis)}
    except FileNotFoundError:
        raise HTTPException(status_code=404, detail="Dados não encontrados")

@app.get("/api/estados")
async def get_estados():
    # Retornar lista de estados disponíveis
    return {"estados": ["SC", "SP", "RS", "PR", "MG", "RJ", "BA", "CE", "PE", "GO", "MT", "MS"]}
```

---

## 📊 **MÉTRICAS DE PROGRESSO**

### **Semana 1**
- [ ] Sistema de logs funcionando
- [ ] Retry automático implementado
- [ ] Bugs críticos corrigidos
- [ ] Testes de estabilidade passando

### **Semana 2**
- [ ] Relatórios HTML gerados
- [ ] Validação de dados implementada
- [ ] 3-5 novos estados adicionados
- [ ] Métricas de qualidade funcionando

### **Semana 3**
- [ ] 5-7 novos estados adicionados
- [ ] Filtros avançados implementados
- [ ] Monitoramento básico funcionando
- [ ] Documentação atualizada

### **Semana 4**
- [ ] Dashboard web básico funcionando
- [ ] API REST implementada
- [ ] Frontend responsivo
- [ ] Integração completa testada

---

## 🚨 **RISCOS E CONTINGÊNCIAS**

### **Riscos Identificados**
1. **Mudanças no site da Caixa**
   - Contingência: Monitoramento contínuo + testes diários

2. **Problemas de performance**
   - Contingência: Otimização de código + cache

3. **Falhas de rede**
   - Contingência: Retry automático + timeouts

4. **Limitações de rate limiting**
   - Contingência: Delays inteligentes + rotação de IPs

### **Planos de Contingência**
- **Backup de código**: Git com branches de backup
- **Dados críticos**: Backup automático diário
- **Infraestrutura**: Múltiplas opções de deploy
- **Equipe**: Documentação para transferência de conhecimento

---

## 📞 **COMUNICAÇÃO E RELATÓRIOS**

### **Relatórios Diários**
- Status das tarefas do dia
- Problemas encontrados
- Próximos passos
- Métricas de progresso

### **Relatórios Semanais**
- Resumo da semana
- Progresso vs. plano
- Ajustes necessários
- Planejamento da próxima semana

### **Canais de Comunicação**
- GitHub Issues para bugs
- Documentação atualizada
- Logs estruturados
- Métricas de performance

---

## 🎯 **CRITÉRIOS DE SUCESSO**

### **Técnicos**
- [ ] 100% dos testes passando
- [ ] Sistema estável (99% uptime)
- [ ] Performance < 30s por busca
- [ ] Cobertura de 20+ estados

### **Funcionais**
- [ ] Dashboard web funcionando
- [ ] Relatórios HTML gerados
- [ ] Filtros avançados implementados
- [ ] API REST disponível

### **Qualidade**
- [ ] Código documentado
- [ ] Logs estruturados
- [ ] Validação de dados
- [ ] Monitoramento ativo

---

**🚀 Este plano de ação detalhado garante que o projeto evolua de forma estruturada e controlada, mantendo a qualidade e estabilidade em todas as etapas.**


