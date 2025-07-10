@echo off
echo ========================================
echo INSTALADOR SCRAPER IMOVEIS CAIXA
echo ========================================
echo.

echo Instalando dependencias...
pip install -r requirements.txt

echo.
echo Instalando o projeto...
pip install -e .

echo.
echo ========================================
echo INSTALACAO CONCLUIDA!
echo ========================================
echo.
echo Para executar o scraper, use:
echo python scraper_simples_interativo.py
echo.
echo Ou simplesmente:
echo scraper-caixa
echo.
pause 