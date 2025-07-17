@echo off
echo ========================================
echo SCRAPER AUTOMATICO - IMOVEIS CAIXA
echo ========================================
echo.
echo Iniciando busca automatica...
echo Data/Hora: %date% %time%
echo.

cd /d "%~dp0"
python scraper_direto.py

echo.
echo ========================================
echo Scraper concluido!
echo Data/Hora: %date% %time%
echo ========================================
echo.
pause 