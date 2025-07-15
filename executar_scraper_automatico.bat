@echo off
echo ========================================
echo SCRAPER AUTOMATICO DE IMOVEIS - CAIXA
echo ========================================
echo.
echo Iniciando busca de imoveis...
echo Data/Hora: %date% %time%
echo.

cd /d "%~dp0"
python scraper_automatico.py

echo.
echo ========================================
echo Scraper concluido!
echo Data/Hora: %date% %time%
echo ========================================
echo.
pause 