@echo off
echo ========================================
echo    CONFIGURACAO SCRAPER CAIXA
echo ========================================
echo.
echo Escolha o modo de execucao:
echo.
echo 1. 🚀 Modo Rapido (sem instalacao)
echo    - Executa diretamente o Python
echo    - Mais rapido para uso frequente
echo.
echo 2. 📦 Modo Completo (com instalacao)
echo    - Instala como comando do sistema
echo    - Melhor para uso profissional
echo.
echo 3. 🔧 Apenas Instalar
echo    - Instala dependencias e comando
echo    - Para uso futuro
echo.
echo 4. ❌ Sair
echo.

set /p escolha="Digite sua escolha (1-4): "

if "%escolha%"=="1" (
    echo.
    echo 🚀 Executando modo rapido...
    call executar_direto.bat
) else if "%escolha%"=="2" (
    echo.
    echo 📦 Executando modo completo...
    call executar_scraper.bat
) else if "%escolha%"=="3" (
    echo.
    echo 🔧 Instalando dependencias...
    call install.bat
) else if "%escolha%"=="4" (
    echo.
    echo 👋 Saindo...
    exit /b 0
) else (
    echo.
    echo ❌ Opcao invalida!
    pause
    goto :eof
) 