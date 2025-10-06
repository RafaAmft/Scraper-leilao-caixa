# ⚠️ CORREÇÃO: Códigos do Distrito Federal

## 🔧 Problema Identificado

Os códigos IBGE do DF **NÃO FUNCIONAM** no site da Caixa!

O site da Caixa usa **códigos internos próprios**, não os códigos IBGE oficiais.

---

## ✅ CÓDIGOS CORRETOS (Verificados no Site)

Após verificação direta no site da Caixa em **06/10/2025**, os códigos corretos do DF são:

| Código | Região Administrativa | Status |
|--------|----------------------|--------|
| **1809** | BRASÍLIA | ✅ Verificado |
| **1820** | CEILÂNDIA | ✅ Verificado |
| **1822** | GAMA | ✅ Verificado |
| **1823** | GUARÁ | ✅ Verificado |
| **1826** | NÚCLEO BANDEIRANTE | ✅ Verificado |
| **1829** | RECANTO DAS EMAS | ✅ Verificado |
| **1831** | SAMAMBAIA | ✅ Verificado |
| **1832** | SANTA MARIA | ✅ Verificado |
| **1834** | SOBRADINHO | ✅ Verificado |
| **1835** | TAGUATINGA | ✅ Verificado |

**Total**: 10 regiões administrativas disponíveis

---

## ❌ Códigos INCORRETOS (Não Funcionam)

Estes códigos IBGE **NÃO EXISTEM** no site da Caixa:

| Código IBGE | Nome | Problema |
|-------------|------|----------|
| ~~5300108~~ | BRASÍLIA | Código IBGE, não aceito pela Caixa |
| ~~5300100~~ | DISTRITO FEDERAL | Código IBGE, não aceito pela Caixa |
| ~~5300109~~ | BRASÍLIA - PLANO PILOTO | Código IBGE, não aceito pela Caixa |
| ~~5300110~~ | TAGUATINGA | Código IBGE, não aceito pela Caixa |
| ~~5300111~~ | CEILÂNDIA | Código IBGE, não aceito pela Caixa |
| ~~5300112~~ | SAMAMBAIA | Código IBGE, não aceito pela Caixa |
| ~~5300113~~ | GAMA | Código IBGE, não aceito pela Caixa |

---

## 🔄 Arquivos Corrigidos

Todos os arquivos foram atualizados com os códigos corretos:

### 1. **`src/scraper_caixa/config.py`**
```python
"DF": {
    "1809": "BRASILIA",
    "1820": "CEILANDIA",
    "1822": "GAMA",
    "1823": "GUARA",
    "1826": "NUCLEO BANDEIRANTE",
    "1829": "RECANTO DAS EMAS",
    "1831": "SAMAMBAIA",
    "1832": "SANTA MARIA",
    "1834": "SOBRADINHO",
    "1835": "TAGUATINGA",
},
```

### 2. **`src/scraper_caixa/scraper.py`**
Atualizado com os mesmos códigos.

### 3. **`configuracao_cidades.json`**
```json
"DF": {
  "1809": "BRASILIA",
  "1820": "CEILANDIA",
  "1822": "GAMA",
  "1823": "GUARA",
  "1826": "NUCLEO BANDEIRANTE",
  "1829": "RECANTO DAS EMAS",
  "1831": "SAMAMBAIA",
  "1832": "SANTA MARIA",
  "1834": "SOBRADINHO",
  "1835": "TAGUATINGA"
}
```

---

## 🧪 Como os Códigos Foram Verificados

Utilizamos o script `verificar_codigos_df.py` que:

1. ✅ Acessa o site da Caixa com Selenium
2. ✅ Seleciona o estado "DF"
3. ✅ Extrai TODOS os códigos disponíveis do dropdown
4. ✅ Compara com nossos códigos configurados
5. ✅ Relata quais são corretos e incorretos

**Resultado**: Encontradas **10 regiões administrativas** disponíveis no site.

---

## 🎯 Como Usar Agora

### Exemplo 1: Buscar em Brasília
```python
from scraper_caixa import buscar_imoveis_caixa

resultados = buscar_imoveis_caixa(
    estados_cidades={"DF": ["1809"]},  # ✅ Código correto
    tipo_imovel="4",
    headless=True
)
```

### Exemplo 2: Buscar em Ceilândia
```python
resultados = buscar_imoveis_caixa(
    estados_cidades={"DF": ["1820"]},  # ✅ Código correto
    tipo_imovel="2",
    headless=True
)
```

### Exemplo 3: Buscar em Várias Regiões
```python
resultados = buscar_imoveis_caixa(
    estados_cidades={
        "DF": [
            "1809",  # Brasília
            "1820",  # Ceilândia
            "1835",  # Taguatinga
        ]
    },
    tipo_imovel="1",
    headless=True
)
```

---

## 📊 Comparação: Códigos IBGE vs Códigos Caixa

| Região | Código IBGE | Código Caixa | Funciona? |
|--------|-------------|--------------|-----------|
| Brasília | 5300108 | **1809** | ✅ Só o código Caixa |
| Ceilândia | 5300111 | **1820** | ✅ Só o código Caixa |
| Gama | 5300113 | **1822** | ✅ Só o código Caixa |
| Taguatinga | 5300110 | **1835** | ✅ Só o código Caixa |
| Samambaia | 5300112 | **1831** | ✅ Só o código Caixa |

**Conclusão**: A Caixa **NÃO usa códigos IBGE** para o DF!

---

## ⚠️ IMPORTANTE

### Por Que os Códigos IBGE Não Funcionam?

1. **Sistema Legado**: O site da Caixa usa códigos internos antigos
2. **Não Padronizado**: Cada estado pode ter sistema de códigos diferente
3. **DF Especial**: Por ser Distrito Federal (não estado), tem tratamento diferente

### Como Descobrir Códigos de Outras Cidades?

Use o script `verificar_codigos_df.py`:

```bash
python verificar_codigos_df.py
```

Este script:
- ✅ Acessa o site real
- ✅ Extrai códigos atuais
- ✅ Compara com configuração
- ✅ Mostra códigos corretos e incorretos

---

## 🧹 Arquivos para Deletar

O arquivo `CIDADES_DF_ADICIONADAS.md` está **DESATUALIZADO** e pode ser deletado.

Ele contém informações **INCORRETAS** sobre códigos IBGE que não funcionam.

---

## 📝 Resumo da Correção

| Item | Antes | Depois |
|------|-------|--------|
| **Total de cidades** | 7 | **10** |
| **Códigos usados** | IBGE | **Caixa** |
| **Funciona?** | ❌ Não | ✅ **Sim** |
| **Brasília** | 5300108 | **1809** |
| **Taguatinga** | 5300110 | **1835** |
| **Ceilândia** | 5300111 | **1820** |

---

## ✅ Status Atual

- ✅ Códigos corrigidos em todos os arquivos
- ✅ 10 regiões administrativas disponíveis
- ✅ Códigos verificados no site real
- ✅ Pronto para uso!

---

## 🎉 Agora Funciona!

Execute o scraper normalmente:

```bash
python scraper_automatico.py
```

Quando solicitado:
1. Digite: **DF**
2. Escolha uma região (1809, 1820, etc.)
3. ✅ **Funcionará corretamente!**

---

**Data da Correção**: 06 de Outubro de 2025  
**Método**: Verificação direta no site da Caixa  
**Script Usado**: `verificar_codigos_df.py`  
**Status**: ✅ **CORRIGIDO E TESTADO**

