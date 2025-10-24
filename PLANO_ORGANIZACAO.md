# 📋 Plano de Organização do Projeto

## 🎯 Objetivo
Organizar a pasta raiz sem quebrar o código, movendo arquivos para estrutura adequada.

## 📂 Estrutura Proposta

```
projeto/
├── .github/              # CI/CD (já existe)
├── src/                  # Código fonte (já existe)
├── docs/                 # Documentação
│   ├── refatoracao/     # Docs da refatoração
│   ├── ci-cd/           # Docs de CI/CD
│   └── roadmap/         # Roadmaps e planos
├── scripts/              # Scripts utilitários
│   ├── verificacao/     # Scripts de verificação
│   ├── busca/           # Scripts de busca de códigos
│   └── testes/          # Scripts de teste
├── resultados/           # Arquivos de saída
│   ├── relatorios/      # Relatórios gerados
│   ├── screenshots/     # Capturas de tela
│   ├── imoveis/         # CSVs e JSONs de imóveis
│   └── logs/            # Logs de execução
├── config/               # Configurações
├── testes/               # Testes automatizados
├── arquivos_antigos/     # Backup de arquivos antigos
└── [arquivos raiz]       # Apenas essenciais
```

## 📦 Arquivos a Mover

### ✅ Para `docs/refatoracao/`:
- REFATORACAO_V1.1.md
- RESUMO_REFATORACAO.md
- RESUMO_FINAL_V1.1.md
- PROGRESSO_REFATORACAO.md
- ESTRUTURA_ORGANIZADA.md
- PLANO_ACAO_DETALHADO.md

### ✅ Para `docs/ci-cd/`:
- CI_CD_CONFIGURACAO.md
- GITHUB_ACTIONS_SETUP.md

### ✅ Para `docs/roadmap/`:
- ROADMAP_PROJETO.md
- ROADMAP_ATUALIZADO_2025.md
- PROXIMOS_PASSOS.md

### ✅ Para `docs/resumos/`:
- RESUMO_EXECUTIVO.md
- RESUMO_EXECUTIVO_ATUALIZADO_2025.md

### ✅ Para `docs/readme/`:
- README_AUTOMATICO.md
- README_EXTRACAO_CAIXA.md
- README_V1.1.md

### ✅ Para `scripts/verificacao/`:
- verificar_codigos_df.py
- verificar_codigos_cidades.py
- visualizar_cidades_df.py
- investigar_*.py (3 arquivos)
- debug_page_structure.py
- encontrar_url_correta.py
- mostrar_cidades_configuradas.py

### ✅ Para `scripts/busca/`:
- buscar_*.py (5 arquivos)
- configurar_cidades_automatico.py

### ✅ Para `scripts/testes/`:
- teste_*.py (5 arquivos)
- testar_*.py (2 arquivos)

### ✅ Para `scripts/antigos/`:
- scraper_automatico_antigo.py
- scraper_direto.py

### ✅ Para `resultados/relatorios/`:
- relatorio_*.txt (todos)
- teste_relatorio_*.txt (todos)

### ✅ Para `resultados/screenshots/`:
- screenshot_*.png (todos)

### ✅ Para `resultados/imoveis/`:
- imoveis_*.csv
- imoveis_*.json

### ✅ Para `resultados/debug/`:
- debug_*.html
- debug_*.png
- pagina_*.html

### ✅ Manter na raiz (essenciais):
- scraper_automatico.py (PRINCIPAL)
- requirements.txt
- requirements-dev.txt
- pyproject.toml
- setup.py
- README.md
- CHANGELOG.md
- CIDADES_DF_CORRIGIDAS.md
- configuracao_cidades.json
- boaspraticas.md
- .gitignore

### ✅ Já organizados:
- src/ (código fonte)
- .github/ (workflows)
- config/ (configs)
- arquivos_antigos/
- arquivos_temporarios/
- Busca_leilao_caixa/
- scraper_imoveis_caixa.egg-info/

## 🔧 Passos da Organização

1. Criar estrutura de pastas
2. Mover arquivos mantendo referências
3. Atualizar .gitignore se necessário
4. Testar que nada quebrou
5. Commit das mudanças

## ⚠️ Cuidados

- NÃO mover arquivos que são importados
- NÃO mover scripts principais
- Manter backup antes de mover
- Testar após organização


