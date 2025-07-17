@echo off
echo ========================================
echo    SCRAPER IMOVEIS CAIXA
echo ========================================
echo.

REM Verificar se o comando está instalado
busca-leilao-caixa --help >nul 2>&1
if %errorlevel% neq 0 (
    echo ⚠️ Comando nao encontrado. Instalando...
    echo.
    echo Instalando dependencias...
    pip install -r requirements.txt
    echo.
    echo Instalando o projeto...
    pip install -e .
    echo.
    echo ✅ Instalacao concluida!
    echo.
) else (
    echo ✅ Comando ja instalado!
    echo.
)

echo 🚀 Executando scraper...
echo.
busca-leilao-caixa

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
echo 💡 Dica: Para evitar reinstalacao, use diretamente:
echo    python src/scraper_caixa/scraper.py
echo.
pause