@echo off
REM ==========================================================================
REM  Executa o scraper sem interacao (usado pelo Agendador de Tarefas).
REM  - Baixa o CSV da Caixa (--metodo auto --headless), gera os relatorios
REM    e envia o e-mail.
REM  - Toda a saida vai para logs\agendador.log
REM  Argumentos extras sao repassados ao scraper, ex.:
REM    agendar_scraper.bat --sem-email
REM ==========================================================================
setlocal

REM Pasta raiz do projeto (este .bat fica em scripts\)
cd /d "%~dp0.."

REM Evita erro de codificacao ao gravar emojis no arquivo de log
set PYTHONUTF8=1
set PYTHONIOENCODING=utf-8

REM Usa o Python do ambiente virtual do projeto, se existir
set "PY=python"
if exist ".venv\Scripts\python.exe" set "PY=.venv\Scripts\python.exe"
if exist "venv\Scripts\python.exe" set "PY=venv\Scripts\python.exe"

if not exist "logs" mkdir "logs"
set "LOG=logs\agendador.log"

echo.>> "%LOG%"
echo ===== Inicio: %date% %time% =====>> "%LOG%"
"%PY%" scraper_automatico.py --metodo auto --headless %* >> "%LOG%" 2>&1
set "CODIGO=%ERRORLEVEL%"
echo ===== Fim: %date% %time% (codigo de saida %CODIGO%) =====>> "%LOG%"

exit /b %CODIGO%
