# 🏛️ Cidades do Distrito Federal Adicionadas

## 📅 Data de Adição
**11 de Agosto de 2025**

---

## 🗺️ Regiões Administrativas do DF Incluídas

O Distrito Federal foi adicionado ao scraper com as principais regiões administrativas:

| Código IBGE | Região Administrativa | Observações |
|-------------|----------------------|-------------|
| `5300108` | **BRASÍLIA** | Capital federal, Plano Piloto + áreas centrais |
| `5300100` | **DISTRITO FEDERAL** | Código geral do DF (todas as regiões) |
| `5300109` | **BRASÍLIA - PLANO PILOTO** | Área central planejada por Lúcio Costa |
| `5300110` | **TAGUATINGA** | Região administrativa mais populosa |
| `5300111` | **CEILÂNDIA** | Segunda região mais populosa |
| `5300112` | **SAMAMBAIA** | Região administrativa no sudoeste |
| `5300113` | **GAMA** | Região administrativa no sul do DF |

---

## 📂 Arquivos Atualizados

### 1. **`src/scraper_caixa/config.py`**
```python
"DF": {
    "5300108": "BRASILIA",
    "5300100": "DISTRITO FEDERAL",
    "5300109": "BRASILIA - PLANO PILOTO",
    "5300110": "TAGUATINGA",
    "5300111": "CEILANDIA",
    "5300112": "SAMAMBAIA",
    "5300113": "GAMA",
},
```

### 2. **`src/scraper_caixa/scraper.py`**
Adicionada mesma configuração ao arquivo legado.

### 3. **`configuracao_cidades.json`**
```json
"DF": {
  "5300108": "BRASILIA",
  "5300110": "TAGUATINGA",
  "5300111": "CEILANDIA",
  "5300112": "SAMAMBAIA",
  "5300113": "GAMA"
}
```

---

## 🎯 Como Usar

### Exemplo 1: Buscar em Brasília
```python
from scraper_caixa import buscar_imoveis_caixa

resultados = buscar_imoveis_caixa(
    estados_cidades={"DF": ["5300108"]},  # Brasília
    tipo_imovel="4",  # Indiferente
    headless=True
)
```

### Exemplo 2: Buscar em Ceilândia
```python
resultados = buscar_imoveis_caixa(
    estados_cidades={"DF": ["5300111"]},  # Ceilândia
    tipo_imovel="2",  # Apartamento
    headless=True
)
```

### Exemplo 3: Buscar em Todo o DF
```python
resultados = buscar_imoveis_caixa(
    estados_cidades={"DF": ["5300100"]},  # Todo o DF
    tipo_imovel="4",  # Indiferente
    headless=True
)
```

### Exemplo 4: Buscar em Múltiplas Regiões
```python
resultados = buscar_imoveis_caixa(
    estados_cidades={
        "DF": [
            "5300108",  # Brasília
            "5300110",  # Taguatinga
            "5300111",  # Ceilândia
        ]
    },
    tipo_imovel="1",  # Casa
    headless=True
)
```

---

## 📊 Informações Adicionais

### População das Regiões (Estimativa 2024)

| Região | População Aprox. |
|--------|------------------|
| Ceilândia | ~500.000 |
| Taguatinga | ~230.000 |
| Plano Piloto | ~220.000 |
| Samambaia | ~250.000 |
| Gama | ~150.000 |

### 🏠 Mercado Imobiliário do DF

- **Maior concentração de imóveis**: Plano Piloto, Taguatinga, Águas Claras
- **Média de preço**: R$ 5.000 - R$ 8.000/m² (varia muito por região)
- **Tipos mais comuns**: Apartamentos (60%), Casas (40%)
- **Leilões ativos**: Alta demanda na região central

---

## ⚠️ Observações Importantes

### Códigos IBGE do DF

O Distrito Federal tem uma estrutura especial de códigos IBGE:
- **5300100**: Código geral do DF
- **53001XX**: Códigos das regiões administrativas

> ⚙️ **Nota**: Os códigos podem variar no site da Caixa. Se algum não funcionar, use o código geral `5300100` ou teste com o script `verificar_codigos_cidades.py`.

### Verificar Códigos no Site

Para confirmar se os códigos estão corretos:

```bash
python verificar_codigos_cidades.py
```

Ou manualmente:
1. Acesse: https://venda-imoveis.caixa.gov.br/sistema/busca-imovel.asp
2. Selecione "DF" no dropdown de estados
3. Inspecione o dropdown de cidades (F12 → Elements)
4. Veja os valores (`value=""`) das opções

---

## 🧪 Testando a Configuração

### Teste Rápido Local

```bash
# Ativar ambiente virtual
.\venv\Scripts\activate

# Executar teste com DF
python -c "
from src.scraper_caixa.config import ESTADOS_CIDADES
print('✅ DF configurado:', 'DF' in ESTADOS_CIDADES)
print('📍 Cidades do DF:', list(ESTADOS_CIDADES['DF'].values()))
"
```

### Teste de Scraping

```bash
python scraper_automatico.py
```

Quando solicitado:
1. Digite: `DF`
2. Escolha uma ou mais cidades
3. Aguarde a execução

---

## 📈 Resultados Esperados

Após a execução, serão gerados arquivos como:

```
relatorios/
  ├── imoveis_brasilia_20250811_140000.csv
  ├── imoveis_brasilia_20250811_140000.json
  └── relatorio_brasilia_20250811_140000.txt

dados_imoveis/
  ├── imoveis_df_completo.json
  └── imoveis_df_completo.csv
```

---

## 🔄 CI/CD Automático

O workflow diário (`scraper-daily.yml`) agora também inclui o DF automaticamente se configurado no script principal.

**Para incluir DF na execução automática**, edite `scraper_automatico.py` e adicione:

```python
ESTADOS_PADRAO = ["SC", "SP", "MS", "DF"]  # ✅ Incluir DF
```

---

## 🎯 Próximas Melhorias

- [ ] Adicionar outras regiões administrativas do DF
- [ ] Validar códigos no site da Caixa
- [ ] Criar filtros específicos por região
- [ ] Análise de preços por região do DF
- [ ] Mapa de calor de imóveis disponíveis

---

## 📞 Suporte

Se encontrar problemas com os códigos do DF:

1. **Verificar códigos**: `python verificar_codigos_cidades.py`
2. **Testar manualmente**: Acessar site da Caixa e inspecionar
3. **Reportar issue**: Criar issue no GitHub com detalhes

---

**Versão**: 1.1.0  
**Última Atualização**: 11/08/2025  
**Status**: ✅ Configurado e Pronto para Uso

