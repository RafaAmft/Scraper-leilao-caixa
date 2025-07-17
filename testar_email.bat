@echo off
chcp 65001 >nul
echo.
echo 🧪 TESTE DE ENVIO DE EMAIL
echo ================================
echo.
echo Este script testa o envio de email com Gmail.
echo.
echo Pressione qualquer tecla para continuar...
pause >nul

python config/teste_envio_email_simples.py

echo.
echo Pressione qualquer tecla para sair...
pause >nul 