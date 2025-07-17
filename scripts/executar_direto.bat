@echo off
echo ========================================
echo    SCRAPER IMOVEIS CAIXA (DIRETO)
echo ========================================
echo.
echo 🚀 Executando scraper diretamente...
echo.

REM Verificar se o Python está instalado
python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo ❌ Python nao encontrado!
    echo Instale o Python primeiro: https://python.org
    pause
    exit /b 1
)

REM Verificar se as dependências estão instaladas
echo 📦 Verificando dependencias...
pip show selenium >nul 2>&1
if %errorlevel% neq 0 (
    echo ⚠️ Dependencias nao encontradas. Instalando...
    pip install -r requirements.txt
    echo ✅ Dependencias instaladas!
    echo.
) else (
    echo ✅ Dependencias ja instaladas!
    echo.
)

echo 🏠 Executando scraper...
python src/scraper_caixa/scraper.py

echo.
echo ========================================
echo    BUSCA CONCLUIDA!
echo ========================================
echo.
echo 📁 Arquivos gerados:
echo - *.csv (dados dos imoveis)
echo - *.json (dados em formato JSON)
echo - *.png (screenshot da pagina)
echo.
pause 